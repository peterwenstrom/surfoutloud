<template>
  <div>
    <b-navbar class="navbar-fixed-top navbar-sol" toggleable>
      <div class="container">
        <b-nav-toggle target="nav_collapse"></b-nav-toggle>
        <div>
          <img class="logo" src="../assets/LogoFull.png"/>
        </div>
        <b-collapse is-nav id="nav_collapse">
          <b-nav is-nav-bar class="ml-auto">
            <router-link tag="b-nav-item" v-if="!authUser.access_token" to="/login">Log in</router-link>
            <router-link tag="b-nav-item" v-if="!authUser.access_token" to="/register">Register</router-link>
            <router-link tag="b-nav-item" v-if="authUser.access_token" to="/dashboard">Dashboard</router-link>
            <b-nav-item-dropdown v-if="authUser.access_token" right-alignment>
              <template slot="text">
                <span style="font-weight: bold; text-transform:capitalize;">{{authUser.username}}</span>
              </template>
              <b-dropdown-item to="/profile">Profile</b-dropdown-item>
              <b-dropdown-item v-on:click="logout">Logout</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-nav>
        </b-collapse>
      </div>
    </b-navbar>
    <div v-if="loading" class="container spinner-div">
      <div class="row">
        <div class="col-lg-4"></div>
        <div class="spinner-container col-lg-4">
          <ring-loader class="loading" :loading="loading" :color="color" :size="size"></ring-loader>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  import RingLoader from 'vue-spinner/src/RingLoader.vue'
  import userAuth from '../user/userAuth'

  export default {
    data() {
      return {
        loading: false,
        color: '#41B883',
        size: '120px',
        margin: '2px',
        radius: '2px'
      }
    },methods: {
      logout() {
        userAuth.logout();
        this.loading = true;
        setTimeout(() => {
          this.loading = false;
          this.$router.push('login');
        }, 1200);
      }
    },
    computed: {
      ...mapGetters({
        authUser: 'authUser'
      })
    },
    components: {
      RingLoader
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
  .loading {
    text-align:center;
    display: inline-block;
  }
  .spinner-div {
    background-color: #fff;
    border-radius: 25px;
    margin-top: 60px;
    margin-bottom: 60px;
  }
  .spinner-container {
    padding-top: 30px;
    padding-bottom: 30px;
  }
</style>
