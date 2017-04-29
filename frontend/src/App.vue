<template>
  <div id="app">
    <div class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <img class="logo" src="./assets/logosurfin.png"/>
        </div>
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
          <ul class="nav navbar-nav navbar-right">
            <li><router-link class="btn" v-if="!user.authenticated" to="/login">Log in</router-link></li>
            <li><router-link class="btn" v-if="!user.authenticated" to="/register">Register</router-link></li>
            <li><router-link class="btn" v-if="user.authenticated" to="/dashboard">Dashboard</router-link></li>
            <li><a v-if="user.authenticated" v-on:click="logout">Logout</a></li>
          </ul>
        </div>
      </div>
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
        this.$router.push('login')
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

<style scoped>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  .logo {
    height: 45px;
    padding-top: 5px;
  }
  a {
    cursor: pointer;
  }
</style>
