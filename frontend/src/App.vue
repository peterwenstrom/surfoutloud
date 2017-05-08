<template>
  <div id="app">
    <top-menu></top-menu>
    <div class="container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
  import TopMenu from './components/TopMenu.vue'
  import axios from 'axios'

  const API_URL = 'http://localhost:5000/';
  const AUTH_URL = API_URL + 'auth';

  export default {
    created () {
      if(localStorage.getItem('authUser') === null) {
        this.$store.dispatch('clearUserObject');
        this.$router.push('login');
      } else {
        const userObject = JSON.parse(localStorage.getItem('authUser'));
        axios.post(AUTH_URL, userObject,
          {headers: {'Authorization': 'Bearer ' + userObject.access_token}}).then( () => {
          this.$store.dispatch('setUserObject', userObject);
          this.$router.push('dashboard');
        }).catch( () => {
          this.$store.dispatch('clearUserObject');
          localStorage.removeItem('authUser');
          this.$router.push('login');
        });
      }
    },
    components: {
        TopMenu
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
</style>
