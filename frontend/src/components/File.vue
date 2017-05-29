<template>
  <div v-on:keyup.esc="closeModal">
    <h5>All files in project</h5>

    {{ emptyList }}

    <table class="table table-striped">

      <thead>
      <tr>
        <th>File type</th>
        <th>File name</th>
        <th>Download</th>
        <th>Preview</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(item,index) in fileArray">
        <td>
          <div v-if="fileTypeArray[index] === 'docx'"><icon name="file-word-o" class="icon"></icon></div>
          <div v-else-if="fileTypeArray[index] === 'img'"><icon name="picture-o" class="icon"></icon></div>
          <div v-else-if="fileTypeArray[index] === 'default'"><icon name="sticky-note-o" class="icon"></icon></div>
        </td>
        <td>
          <p>{{ item }}</p>
        </td>
        <td>
          <div v-on:click="downloadFile(item, 'download')">
            <icon name="cloud-download" class="icon pointer download"></icon>
          </div>
        </td>
        <td>
          <div v-on:click="downloadFile(item, 'preview')">
            <icon name="eye" class="icon pointer preview"></icon>
          </div>
        </td>
      </tr>
      </tbody>
    </table>

    <form>
      <div>
        <label class="upload" for="file">
          <icon name="cloud-upload" class="icon pointer"></icon>
          <a>Choose a file to upload</a>
        </label>
      </div>
      <input type="file" name="file" id="file" v-on:change="postFile">
    </form>


    <div id="wrapper" class="container">
      <modal v-if="showModal">
        <h3 slot="header" class="modal-title">
          Preview
        </h3>
        <div slot="header" v-on:click="closeModal">
          <icon name="window-close-o" class="pointer"></icon>
        </div>
        <div slot="body">
          <img v-bind:src="imgUrl" class="preview-image">
        </div>

        <div slot="footer">
          <button class="btn btn-outline-info pointer" v-on:click="closeModal()"> Close </button>
        </div>
      </modal>
    </div>


  </div>
</template>

<script>
  import axios from 'axios'
  import FileSaver from 'file-saver'
  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/file-word-o'
  import 'vue-awesome/icons/picture-o'
  import 'vue-awesome/icons/sticky-note-o'
  import 'vue-awesome/icons/cloud-download'
  import 'vue-awesome/icons/cloud-upload'
  import 'vue-awesome/icons/window-close-o'
  import 'vue-awesome/icons/eye'
  import Modal from './Modal'

  export default {
    props: ['projectId'],
    data(){
      return{
        fileTobeUploaded: '',
        projectFolder: '/' + this.projectId + '/',
        allFiles: '',
        fileArray: [],
        fileTypeArray: [],
        fileToBeDownloaded: '',
        fileName: '',
        emptyList: '',
        imgUrl: '',
        showModal: false
      }
    },
    methods: {
      postFile: function (e){
        //TODO: make validation on file upload so that users cannot upload files with non utf-8 chars
        const dropbox_api_arg = JSON.stringify({
          path: this.projectFolder +  e.target.files[0].name,
          mode: 'add',
          autorename: true,
          mute: false
        });

        axios.post('https://content.dropboxapi.com/2/files/upload', e.target.files[0] , {
            headers: {
              'Authorization': 'Bearer ' + '6iPEx2do24gAAAAAAAAD02_spJoubKwILe3QSh2w-W7PZntnbepMw7Dgov3lD7Nk',
              'Content-Type': 'application/octet-stream', //application/octet-stream, which is used for arbitrary binary data.
              'Dropbox-API-Arg': dropbox_api_arg
            }
          }
        ).then( () => {
          this.emptyList = '';
          this.getFiles()
        }).catch( error => {
          console.log(error);
          this.error = error
        });

      },
      getFiles: function(){
        axios.get('https://api.dropboxapi.com/1/metadata/auto/?' + 'path=' + this.projectFolder, {
            headers: {
              'Authorization': 'Bearer ' + '6iPEx2do24gAAAAAAAAD02_spJoubKwILe3QSh2w-W7PZntnbepMw7Dgov3lD7Nk'
            }
          }
        ).then( response => {
          this.fileArray = [];
          for(let i = 0; i < response.data.contents.length; i++){
            let filePath = response.data.contents[i].path;
            this.fileName = filePath.split("/");
            this.fileArray.push(this.fileName[2]);

            let fileEnd = this.fileName[2].split(".");

            if (fileEnd[1] === 'docx'){
              this.fileTypeArray.push('docx');
            }else if (fileEnd[1] === 'jpeg' || fileEnd[1] ==='png' || fileEnd[1] ==='jpg' ){
              this.fileTypeArray.push('img');
            } else {
              this.fileTypeArray.push('default');
            }
          }

        }).catch( error => {
          this.error = error;
          this.emptyList = 'The file list is empty, why not add a file? :)'
        });
      },
      downloadFile: function(fileName, type) {
        let xhr = new XMLHttpRequest();
        xhr.responseType = 'arraybuffer';

        xhr.onload = function() {
          if (xhr.status === 200) {
            console.log(xhr.response);
            if(type==='download'){
              let blob = new Blob([xhr.response], {type: 'application/octet-stream'});
              console.log("xhrresponse");
              console.log(xhr.response);
              FileSaver.saveAs(blob, fileName, true);
            } else if(type === 'preview'){
              this.imgUrl = "data:"+xhr.getResponseHeader("Content-Type")+";base64," + btoa(String.fromCharCode.apply(null, new Uint8Array(xhr.response)));
              this.showModal = true;
            }
          }else {
            let errorMessage = xhr.response || 'Unable to download file';
          }
        }.bind(this);

        xhr.open('POST', 'https://content.dropboxapi.com/2/files/download');
        xhr.setRequestHeader('Authorization', 'Bearer ' + '6iPEx2do24gAAAAAAAAD02_spJoubKwILe3QSh2w-W7PZntnbepMw7Dgov3lD7Nk');
        xhr.setRequestHeader('Dropbox-API-Arg', JSON.stringify({
          path: this.projectFolder + fileName
        }));
        xhr.send();
      },
      closeModal() {
        this.showModal = false;
      }

    },
    mounted(){
      if (!this.projectId) {
        setTimeout( () => {
          this.projectFolder = '/' + this.projectId + '/';
          this.getFiles()
        }, 1200);
      } else {
        this.getFiles()
      }

    },
    components: {
      Icon,
      Modal
    }
  }
</script>

<style scoped>
  th {
    text-align: center;
  }
  td {
    vertical-align: middle;
  }
  td * {
    vertical-align: middle;
    margin-top: 0;
    margin-bottom: 0;
  }
  .upload {
    cursor: pointer;
    border: 1px solid #878787;
    border-radius: 20px;
    padding: 5px 10px 5px 10px;
  }
  .upload:hover svg {
    color: #41B883;
  }
  .upload svg {
    margin: 0px 10px 0px 0px;
  }
  .upload * {
    vertical-align: middle;
  }
  #file {
    display: none;
  }
  .icon {
    width: 20px;
    height: 20px;
    margin: 5px;
  }
  .pointer {
    cursor: pointer;
  }
  .download:hover {
    color: darkorange;
  }
  .preview:hover {
    color: #2973b7;
  }
  .preview-image {
    max-width: 570px;
    max-height: 400px
  }

</style>
