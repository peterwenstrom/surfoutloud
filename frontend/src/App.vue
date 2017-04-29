<template>
  <div id="app">
    <img src="./assets/logosurfin.png"/>
    <div class="container">
      <ul class="nav navbar-nav inner">
        <router-link tag="button" class="btn" v-if="!user.authenticated" to="/login">Log in</router-link>
        <router-link tag="button" class="btn" v-if="!user.authenticated" to="/register">Register</router-link>
        <router-link tag="button" class="btn" v-if="user.authenticated" to="/dashboard">Dashboard</router-link>
        <button class="btn" v-if="user.authenticated" v-on:click="logout">Logout</button>
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
    },
    mounted() {
        if (auth.user.authenticated) {
            this.$router.push('dashboard')
        } else {
            this.$router.push('login')
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
