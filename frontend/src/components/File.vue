<template>
  <div>
    <h5>All files in project</h5>

    {{ emptyList }}

    <table class="table table-striped">

      <thead>
      <tr>
        <th>File type</th>
        <th>File name</th>
        <th>Download</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(item,index) in fileArray">
        <td>
          <div v-if="fileTypeArray[index] === 'docx'"><icon name="file-word-o" class="thumbnail"></icon></div>
          <div v-else-if="fileTypeArray[index] === 'img'"><icon name="picture-o" class="thumbnail"></icon></div>
          <div v-else-if="fileTypeArray[index] === 'default'"><icon name="sticky-note-o" class="thumbnail"></icon></div>
        </td>
        <td>
          <p>{{ item }}</p>
        </td>
        <td>
          <div v-on:click="downloadFile(item)"><icon  name="cloud-download" class="thumbnail point hover"></icon></div>
        </td>
      </tr>
      </tbody>
    </table>

    <form>
      <div>
        <label class="upload" for="file">
          <icon name="cloud-upload" class="thumbnail"></icon>
          <a>Choose a file to upload</a>
        </label>
      </div>
      <input type="file" name="file" id="file" class="point" v-on:change="postFile">
    </form>
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
        thumbNail: '',
        emptyList: ''
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
            }else if (fileEnd[1] === 'jpeg' || 'png' || 'jpg' ){
              this.fileTypeArray.push('img');
            } else {
              this.fileTypeArray.push('default');
            }


          }

          console.log(response.data);

        }).catch( error => {
            this.error = error;
          this.emptyList = 'The file list is empty, why not add a file? :)'
        });
      },

//
      /// funkar inte...

      /*      downloadFile: function(fileName) {



       axios.get('https://content.dropboxapi.com/2/files/download', {
       headers: {
       'Authorization': 'Bearer ' + '6iPEx2do24gAAAAAAAAD02_spJoubKwILe3QSh2w-W7PZntnbepMw7Dgov3lD7Nk',
       'Dropbox-API-Arg': JSON.stringify({
       path: this.projectFolder + fileName
       })

       }
       }
       ).then( response => {
       //TODO: Save response to users computer!


       let fileTag = fileName.split(".");
       console.log("this.filename");
       console.log(fileName);
       console.log("response");
       console.log(Object.values(response.headers)[1]);




       let blob = new Blob([Object.values(response.headers)[1]], {type: "application/octet-stream"})
       console.log("blob: ");
       console.log(blob);

       FileSaver.saveAs(blob, fileName, true);


       });



       },*/
      downloadFile: function(fileName) {
        let xhr = new XMLHttpRequest();
        xhr.responseType = 'arraybuffer';

        xhr.onload = function() {
          if (xhr.status === 200) {
            let blob = new Blob([xhr.response], {type: 'application/octet-stream'});
            console.log("xhrresponse");
            console.log(xhr.response);
            FileSaver.saveAs(blob, fileName, true);
          }
          else {
            let errorMessage = xhr.response || 'Unable to download file';
          }
        };

        xhr.open('POST', 'https://content.dropboxapi.com/2/files/download');
        xhr.setRequestHeader('Authorization', 'Bearer ' + '6iPEx2do24gAAAAAAAAD02_spJoubKwILe3QSh2w-W7PZntnbepMw7Dgov3lD7Nk');
        xhr.setRequestHeader('Dropbox-API-Arg', JSON.stringify({
          path: this.projectFolder + fileName
        }));
        xhr.send();
      },


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
    }
  }
</script>

<style scoped>
  th {
    text-align: center;
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
  .thumbnail {
    width: 20px;
    height: 20px;
    margin: 5px;
  }

  .point {
    cursor: pointer;
  }

  .hover:hover {
    color: darkorange;
  }
</style>
