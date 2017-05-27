<template>
  <div>
    <h4>All files in project</h4>
    <tr v-for="item in fileArray">
      <td>
        <p>{{ item }}</p>
      </td>
    </tr>
    <form>
      <input type="file" name="file" id="file" v-on:change="postFile">
    </form>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    data(){
      return{
        fileTobeUploaded: '',
        projectFolder: 'templateproject',
        allFiles: '',
        fileArray: []
      }
    },
    methods: {
      postFile: function (e){
        //TODO: make validation on file upload so that users cannot upload files with non utf-8 chars
        console.log(e.target.files[0]);

        const dropbox_api_arg = JSON.stringify({
          path: '/' + this.projectFolder + '/' +  e.target.files[0].name,
          mode: 'add',
          autorename: true,
          mute: false
        });

        axios.post('https://content.dropboxapi.com/2/files/upload', e.target.files[0] , {
            headers: {
              'Authorization': 'Bearer ' + '6iPEx2do24gAAAAAAAAD02_spJoubKwILe3QSh2w-W7PZntnbepMw7Dgov3lD7Nk',
              'Content-Type': 'application/octet-stream',
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
        axios.get('https://api.dropboxapi.com/1/metadata/auto/?' + 'path=/templateproject/', {
            headers: {
              'Authorization': 'Bearer ' + '6iPEx2do24gAAAAAAAAD02_spJoubKwILe3QSh2w-W7PZntnbepMw7Dgov3lD7Nk'
            }
          }
        ).then( response => {
          this.fileArray = [];
          for(let i = 0; i < response.data.contents.length; i++){
            this.fileArray.push(response.data.contents[i].path);
          }

          console.log(response.data.contents[0].path);
          if (response.data.kind === 'file') {
            let blob = response.data.getAsFile();
            let reader = new FileReader();
            reader.onload = function(event){
              console.log(event.target.result)
            }; // data url!
            reader.readAsDataURL(blob);

          }

        });
      }
      ,
      downloadFile: function(evt, file) {
        evt.preventDefault();
        let xhr = new XMLHttpRequest();
        xhr.responseType = 'arraybuffer';

        xhr.onload = function() {
          if (xhr.status === 200) {
            let blob = new Blob([xhr.response], {type: 'application/octet-stream'});
            FileSaver.saveAs(blob, file.name, true);
          }
          else {
            let errorMessage = xhr.response || 'Unable to download file';
            // Upload failed. Do something here with the error.
          }
        };

        xhr.open('POST', 'https://content.dropboxapi.com/2/files/download');
        xhr.setRequestHeader('Authorization', 'Bearer ' + '6iPEx2do24gAAAAAAAAD02_spJoubKwILe3QSh2w-W7PZntnbepMw7Dgov3lD7Nk');
        xhr.setRequestHeader('Dropbox-API-Arg', JSON.stringify({
          path: this.projectFolder + '/' + file
        }));
        xhr.send();
      }


    },
    created(){
      this.getFiles();
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
</style>
