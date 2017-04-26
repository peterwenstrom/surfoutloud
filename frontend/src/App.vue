<template>
  <div id="app">
    <img src="./assets/logosurfin.png"/>
    <div class="container">
      <ul class="nav navbar-nav inner">
        <router-link tag="button" class="btn" v-if="!user.authenticated" to="/login">Log in</router-link>
        <router-link tag="button" class="btn" v-if="!user.authenticated" to="/register">Register</router-link>
        <router-link tag="button" class="btn" v-if="user.authenticated" to="/Hello">Hello</router-link>
        <router-link tag="button" class="btn" v-if="user.authenticated" to="/Bye">Good Bye</router-link>
        <router-link tag="button" class="btn" v-if="user.authenticated" to="/Chat">Go to chat</router-link>
        <router-link tag="button" class="btn" v-if="user.authenticated" to="/ProjectView">Go to projectview</router-link>
      </ul>
    </div>
    <div class="container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
  import auth from './auth'
export default {
    data() {
      return {
        user: auth.user
      }
    },
    methods: {
      logout() {
        auth.logout()
      }
    }
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
