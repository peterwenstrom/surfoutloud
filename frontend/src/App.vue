<template>
  <div id="app">
    <img src="./assets/logosurfin.png"/>
    <div class="container">
      <ul class="nav navbar-nav inner">
        <router-link tag="button" class="btn" to="/login">Log in</router-link>
        <router-link tag="button" class="btn" to="/register">Register</router-link>
        <router-link tag="button" class="btn" to="/Hello">Hello</router-link>
        <router-link tag="button" class="btn" to="/Bye">Good Bye</router-link>
        <router-link tag="button" class="btn" to="/Chat">Go to chat</router-link>
        <router-link tag="button" class="btn" to="/ProjectView">Go to projectview</router-link>
      </ul>
    </div>
    <div class="container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.inner {
  float: none;
}
</style>
