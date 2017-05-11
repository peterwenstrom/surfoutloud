<template>
  <div class="row">
    <div class="col-md-4"></div>
    <div class="col-md-4">
      <div v-if="!loading">
        <img class="logo" src="../assets/LogoText.png"/>
        <h2>Register</h2>
        <p>Register here if you don't have an account</p>
        <div class="alert alert-danger" v-if="error">
          <p>{{ error }}</p>
        </div>
        <div class="form-group">
          <input
            type="text"
            class="form-control"
            placeholder="Enter your username"
            v-model="credentials.username"
            v-on:keyup.enter="submit"
          >
        </div>
        <div class="form-group">
          <input
            id="password"
            type="password"
            class="form-control"
            placeholder="Enter your password"
            v-model="credentials.password"
            v-on:keyup.enter="submit"
          >
        </div>
        <div class="form-group">
          <input
            id="repeat-password"
            type="password"
            class="form-control"
            placeholder="Repeat your password"
            v-model="credentials.repeat_password"
            v-on:keyup.enter="submit"
          >
        </div>
        <button class="register-btn btn" v-on:click="submit">Register</button>
      </div>
      <ring-loader class="loading" v-if="loading" :loading="loading" :color="color" :size="size"></ring-loader>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import RingLoader from 'vue-spinner/src/RingLoader.vue'
  import userAuth from '../user/userAuth'

  export default {
    data() {
      return {
        credentials: {
          username: '',
          password: '',
          repeat_password: ''
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
      submit() {
        let credentials = {
          username: this.credentials.username,
          password: this.credentials.password,
          repeat_password: this.credentials.repeat_password
        };
        if (credentials.password === credentials.repeat_password) {
          this.loading = true;
          userAuth.register(credentials, error => {
            if (error) {
              this.error = error;
            } else {
              this.$router.push('dashboard');
            }
            this.loading = false;
          });
        } else {
          this.error = 'The passwords are not identical, please try again'
        }
      }
    },
    components: {
      RingLoader
    }

  }
</script>

<style scoped>
  .register-btn {
    background-color: #35495E;
    color: #fff;
  }
  .loading {
    text-align:center;
    display: inline-block;
  }
</style>
