<template>
  <div>
    <b-navbar class="navbar-fixed-top navbar-sol" toggleable>
      <div class="container">
        <b-nav-toggle target="nav_collapse"></b-nav-toggle>
        <div>
          <img class="logo" src="../assets/logosurfin.png"/>
        </div>
        <b-collapse is-nav id="nav_collapse">
          <b-nav is-nav-bar class="ml-auto">
            <router-link tag="b-nav-item" v-if="!authUser.access_token" to="/login">Log in</router-link>
            <router-link tag="b-nav-item" v-if="!authUser.access_token" to="/register">Register</router-link>
            <router-link tag="b-nav-item" v-if="authUser.access_token" to="/dashboard">Dashboard</router-link>
            <b-nav-item-dropdown v-if="authUser.access_token" right-alignment>
              <template slot="text">
                <span style="font-weight: bold;">{{authUser.username}}</span>
              </template>
              <b-dropdown-item to="#">Profile</b-dropdown-item>
              <b-dropdown-item v-on:click="logout">Logout</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-nav>
        </b-collapse>
      </div>
    </b-navbar>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'

  export default {
    methods: {
      logout() {
        localStorage.removeItem('authUser');
        this.$store.dispatch('clearUserObject');
        setTimeout(() => {
          this.$router.push('login');
        }, 1000);
      }
    },
    computed: {
      ...mapGetters({
        authUser: 'authUser'
      })
    }
  }

</script>

<style scoped>
  .logo {
    height: 45px;
    padding-top: 5px;
  }
  .navbar-sol {
    background-color: #c6c6c6;
    border-bottom: thick solid #878787;
  }
  .ml-auto > li {
    margin: 0px 15px 0px 15px;
  }
</style>
