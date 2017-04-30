<template>
  <div id="app">
    <b-navbar class="navbar-fixed-top navbar-sol" toggleable>
      <div class="container">
        <b-nav-toggle target="nav_collapse"></b-nav-toggle>
        <div>
          <img class="logo" src="./assets/logosurfin.png"/>
        </div>
        <b-collapse is-nav id="nav_collapse">
          <b-nav is-nav-bar class="ml-auto">
            <router-link tag="b-nav-item" v-if="!user.authenticated" to="/login">Log in</router-link>
            <router-link tag="b-nav-item" v-if="!user.authenticated" to="/register">Register</router-link>
            <router-link tag="b-nav-item" v-if="user.authenticated" to="/dashboard">Dashboard</router-link>
            <b-nav-item-dropdown v-if="user.authenticated" right-alignment>
              <template slot="text">
                <span style="font-weight: bold;">User</span>
              </template>
              <b-dropdown-item to="#">Profile</b-dropdown-item>
              <b-dropdown-item v-if="user.authenticated" v-on:click="logout">Logout</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-nav>
        </b-collapse>
      </div>
    </b-navbar>

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
        auth.logout();
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
  }
  .logo {
    height: 45px;
    padding-top: 5px;
  }
  .navbar-sol {
    background-color: #c6c6c6;
    border-bottom: thick solid #878787;
    margin-bottom: 20px;
  }
  .ml-auto > li {
    margin: 0px 15px 0px 15px;
  }
</style>
