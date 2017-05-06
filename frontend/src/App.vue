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

  export default {
    created () {
      if(localStorage.getItem('authUser') !== null) {
          const userObject = JSON.parse(localStorage.getItem('authUser'));
          this.$store.dispatch('setUserObject', userObject);
          this.$router.push('dashboard');
      } else {
          this.$store.dispatch('clearUserObject');
          this.$router.push('login');
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
