<template>
  <div id="app">
    <top-menu></top-menu>
    <div class="container main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
  import TopMenu from './components/shared_components/TopMenu.vue'
  import axios from 'axios'

  export default {
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
    border-radius: 5px;
    margin-top: 60px;
    margin-bottom: 60px;
  }
  .main-content div {
    padding-top: 30px;
    padding-bottom: 30px;
  }
</style>
