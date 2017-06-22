<template>
  <div class="row">
    <div class="col-lg-4 col-sm-2"></div>
    <div class="col-lg-4 col-sm-8">
      <div v-if="!loading">
        <img class="logo" src="../assets/LogoText.png"/>
        <h2>Log in</h2>
        <p>Log in if you already have an account</p>
        <div class="alert alert-danger" v-if="error">
          <p>{{ error }}</p>
        </div>
        <div class="form-group">
          <input
            type="text"
            class="form-control"
            placeholder="Enter your username"
            v-model="credentials.username"
            v-on:keyup.enter="login"
          >
        </div>
        <div class="form-group">
          <input
            type="password"
            class="form-control"
            placeholder="Enter your password"
            v-model="credentials.password"
            v-on:keyup.enter="login"
          >
        </div>
        <button class="login-btn btn" v-on:click="login">Log in</button>
      </div>
      <ring-loader class="loading" v-if="loading" :loading="loading" :color="color" :size="size"></ring-loader>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import RingLoader from 'vue-spinner/src/RingLoader.vue'
  import userAuth from '../store/user/userAuth'

  export default {
    data() {
      return {
        credentials: {
          username: '',
          password: ''
        },
        error: '',
        loading: false,
        color: '#41B883',
        size: '120px',
        margin: '2px',
        radius: '2px'
      }
    },
    methods: {
      login() {
        let credentials = {
          username: this.credentials.username,
          password: this.credentials.password
        };
        this.loading = true;
        userAuth.login(credentials, error => {
          if(error) {
            this.error = error;
          } else {
            this.$router.push('dashboard');
          }
          this.loading = false;
        });
      }
    },
    components: {
      RingLoader
    }
  }
</script>

<style scoped>
  .login-btn {
    background-color: #41B883;
    color: #fff;
    cursor: pointer;
  }
  .loading {
    text-align:center;
    display: inline-block;
  }
</style>
