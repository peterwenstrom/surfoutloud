<template>
  <div>
    <b-navbar class="navbar-fixed-top navbar-sol" toggleable>
      <div class="container">
        <b-nav-toggle target="nav_collapse"></b-nav-toggle>
        <div v-on:click="linkToDashboard">
          <img class="logo" src="../assets/LogoFull.png"/>
        </div>
        <b-collapse is-nav id="nav_collapse">
          <b-nav is-nav-bar class="ml-auto">
            <router-link tag="b-nav-item" v-if="!authorized" to="/login">Log in</router-link>
            <router-link tag="b-nav-item" v-if="!authorized" to="/register">Register</router-link>
            <b-nav-item v-if="authorized" v-on:click="linkToDashboard">Dashboard</b-nav-item>
            <b-nav-item-dropdown v-if="authorized" right-alignment>
              <template slot="text">
                <span class="menu-name">{{user.username}}</span>
              </template>
              <router-link tag="b-dropdown-item" to="/profile">Profile</router-link>
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
  import userAuth from '../user/userAuth'

  export default {
    data() {
      return {
      }
    },
    methods: {
      logout() {
        userAuth.logout();
      },
      linkToDashboard() {
        // Somewhat customised routing to enable reload of page if dashboard or logo is
        // clicked even though you currently are on the dashboard.
        if (window.location.hash === '#/dashboard') {
          this.$store.dispatch('setUpdateProjects', true)
        } else {
          this.$router.push('/dashboard')
        }
      }
    },
    computed: {
      ...mapGetters({
        user: 'user',
        authorized: 'authorized'
      })
    }
  }

</script>

<style scoped>
  .logo {
    height: 45px;
    padding-top: 5px;
    cursor: pointer;
  }
  .navbar-sol {
    background-color: #c6c6c6;
    border-bottom: thick solid #878787;
  }
  .ml-auto > li {
    margin: 0px 15px 0px 15px;
  }
  .menu-name {
    font-weight: bold;
    text-transform: capitalize;
  }
</style>
