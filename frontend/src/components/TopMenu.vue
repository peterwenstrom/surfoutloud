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
              <b-dropdown-item to="#">Profile</b-dropdown-item>
              <b-dropdown-item v-on:click="logout">Logout</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-nav>
        </b-collapse>
      </div>
    </b-navbar>
    <div v-if="loading" class="row">
      <div class="col-sm-4"></div>
      <div class="col-sm-4">
        <grid-loader style="margin-left:40%;" v-if="loading" :loading="loading" :color="color" :size="size"></grid-loader>
      </div>
    </div>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  import GridLoader from 'vue-spinner/src/GridLoader.vue'

  export default {
    data() {
      return {
        loading: false,
        color: '#41B883',
        size: '30px',
        margin: '2px',
        radius: '2px'
      }
    },methods: {
      logout() {
        localStorage.removeItem('authUser');
        this.$store.dispatch('clearUserObject');
        this.loading = true;
        setTimeout(() => {
          this.loading = false;
          this.$router.push('login');
        }, 1000);
      }
    },
    computed: {
      ...mapGetters({
        authUser: 'authUser'
      })
    },
    components: {
      GridLoader
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
