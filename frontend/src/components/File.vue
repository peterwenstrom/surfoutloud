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

          <button v-on:click="downloadFile(item, 'preview')">Preview</button>
          <div v-if="fileTypeArray[index] === 'docx'"><icon name="file-word-o" class="thumbnail"></icon></div>
          <div v-else-if="fileTypeArray[index] === 'img'"><icon name="picture-o" class="thumbnail"></icon></div>
          <div v-else-if="fileTypeArray[index] === 'default'"><icon name="sticky-note-o" class="thumbnail"></icon></div>
        </td>
        <td>
          <p>{{ item }}</p>
        </td>
        <td>
          <div v-on:click="downloadFile(item, 'download')"><icon  name="cloud-download" class="thumbnail point hover"></icon></div>
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

    <img id="imgPreviewFake" v-bind:src="imgUrl" style="display: none" class="image center">

     <modal name="preview"
             :resizeable="true"
             :width="400"
             :height="parseInt(modalHeight)"
              @before-open="beforeOpen"
      >
        <div v-if="imgUrl" class="parent">
          <img id="imgPreview" v-bind:src="imgUrl" class="image center">
        </div>
      </modal>

  </div>
</template>

<script>
  import Vue from 'vue'
  import axios from 'axios'
  import FileSaver from 'file-saver'
  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/file-word-o'
  import 'vue-awesome/icons/picture-o'
  import 'vue-awesome/icons/sticky-note-o'
  import 'vue-awesome/icons/cloud-download'
  import vmodal from 'vue-js-modal'
  Vue.use(vmodal)
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
        emptyList: '',
        imgUrl: '',
        modalWidth: '',
        modalHeight: '',
        showModal: false
      }
    },
    methods: {
      postFile: function (e){
        //TODO: make validation on file upload so that users cannot upload files with non utf-8 chars
        console.log(e.target.files[0]);

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
        ).then( response => {
          console.log(response);

          this.getFiles();

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
            console.log(response);
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
              //console.log(this.imgUrl);

              setTimeout(function() {
                this.modalWidth = document.getElementById('imgPreviewFake').clientWidth;
                this.modalHeight = document.getElementById('imgPreviewFake').clientHeight;


                              console.log("modalheight: ");
                console.log(this.modalHeight);
                console.log("modalwidth: ");
                console.log(this.modalWidth);


              this.$nextTick(() => {

                this.$modal.show('preview');


              });

              }.bind(this),1000)




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
      beforeOpen: function() {

      }

    },
    created(){
      this.getFiles();
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

  .center {
    display: inline-block;
  }

  .parent {
    width: 100%;

    text-align: center;
  }

  .changeWidth {
    width: 300px;
  }






</style>
