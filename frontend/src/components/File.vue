<template>
  <div>
    <h4>All files in project</h4>
    <tr v-for="item in fileArray">
      <td>
        <img v-bind:src="thumbNail" class="thumbnail"><a v-on:click="downloadFile(item)">{{ item }}</a>
      </td>
    </tr>
    <form>
      <input type="file" name="file" id="file" v-on:change="postFile">
    </form>
  </div>
</template>

<script>
  import axios from 'axios'
  import FileSaver from 'file-saver'
  export default {
    data(){
      return{
        fileTobeUploaded: '',
        projectFolder: '/templateproject/',
        allFiles: '',
        fileArray: [],
        fileToBeDownloaded: '',
        fileName: '',
        thumbNail: ''
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
          }

          console.log(response.data);

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

      getThumbNails: function() {

        let xhr = new XMLHttpRequest();
        xhr.responseType = 'blob';

        xhr.onload = function(e) {
          if (xhr.status === 200) {
            let blob = new Blob([xhr.response], {type: 'application/octet-stream'});
            console.log("xhrresponse");
            console.log(xhr.response);

            let urlCreator = window.URL || window.webkitURL;

            this.thumbNail = urlCreator.createObjectURL(this.response);
            console.log("thumbNail");
            console.log(this.thumbNail);
            //FileSaver.saveAs(blob, fileName, true);
          }
          else {
            let errorMessage = xhr.response || 'Unable to download file';
          }
        };

        xhr.open('POST', 'https://content.dropboxapi.com/2/files/get_thumbnail');
        xhr.setRequestHeader('Authorization', 'Bearer ' + '6iPEx2do24gAAAAAAAAD02_spJoubKwILe3QSh2w-W7PZntnbepMw7Dgov3lD7Nk');
        xhr.setRequestHeader('Dropbox-API-Arg', JSON.stringify({
          path: 'rev:9381e76314d',
          format: "jpeg",
          size: 'w64h64'
        }));
        xhr.send();
      }




    },
    created(){
      this.getFiles();
      this.getThumbNails();
    }
  }
</script>

<style scoped>

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
  .main-content {
    background-color: #fff;
    border-radius: 25px;
    margin-top: 60px;
    margin-bottom: 60px;
  }
  .main-content div {
    padding-top: 30px;
    padding-bottom: 30px;
  }

  .thumbnail {
    width: 64px;
    height: 64px;
    float: left;
    margin: 5px;
  }
</style>
