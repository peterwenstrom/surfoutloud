<template>
  <div id="app">
    <top-menu></top-menu>
    <div class="container main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
  import TopMenu from './components/TopMenu.vue'
  import axios from 'axios'

  const AUTH_URL = '/api/auth';

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
