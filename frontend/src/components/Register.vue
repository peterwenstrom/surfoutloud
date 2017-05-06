<template>
  <div class="row">
    <div class="col-sm-4"></div>
    <div class="col-sm-4">
      <div v-if="!loading">
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
        <button class="register-btn btn" v-on:click="submit">Register</button>
      </div>
      <grid-loader style="margin-left:40%;" v-if="loading" :loading="loading" :color="color" :size="size"></grid-loader>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import GridLoader from 'vue-spinner/src/GridLoader.vue'

  const API_URL = 'http://localhost:5000/';
  const REGISTER_URL = API_URL + 'register';

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
        size: '30px',
        margin: '2px',
        radius: '2px'
      }
    },
    methods: {
      submit() {
        let credentials = {
          username: this.credentials.username,
          password: this.credentials.password
        };
        this.loading = true;
        axios.post(REGISTER_URL, credentials).then(response => {
          localStorage.setItem('authUser', JSON.stringify(response.data));
          this.$store.dispatch('setUserObject', response.data);
          this.$router.push('dashboard');
        }).catch(err => {
          this.error = err.response.data.message;
          this.loading = false;
        });
      }
    },
    components: {
        GridLoader
    }

  }
</script>

<style scoped>
  .register-btn {
    background-color: #35495E;
    color: #fff;
  }
</style>
