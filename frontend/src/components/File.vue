<template>
  <div>
    <h4>All files in project</h4>
    <tr v-for="item in fileArray">
      <td>
        <a v-on:click="downloadFile(item)">{{ item }}</a>
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
        projectFolder: '/templateproject/',
        allFiles: '',
        fileArray: [],
        fileToBeDownloaded: ''
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
        axios.get('https://api.dropboxapi.com/1/metadata/auto/?' + 'path=' + this.projectFolder, {
            headers: {
              'Authorization': 'Bearer ' + '6iPEx2do24gAAAAAAAAD02_spJoubKwILe3QSh2w-W7PZntnbepMw7Dgov3lD7Nk'
            }
          }
        ).then( response => {
          this.fileArray = [];
          for(let i = 0; i < response.data.contents.length; i++){
            let filePath = response.data.contents[i].path;
            let fileName = filePath.split("/");
            this.fileArray.push(fileName[2]);
          }

          console.log(response.data);

        });
      }
      ,
      downloadFile: function(file) {
        


        axios.get('https://content.dropboxapi.com/2/files/download', {
            headers: {
              'Authorization': 'Bearer ' + '6iPEx2do24gAAAAAAAAD02_spJoubKwILe3QSh2w-W7PZntnbepMw7Dgov3lD7Nk',
              'Dropbox-API-Arg': JSON.stringify({
                path: this.projectFolder + file
              })

            }
          }
        ).then( response => {
        //TODO: Save response to users computer!
          console.log(response);

        });



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
