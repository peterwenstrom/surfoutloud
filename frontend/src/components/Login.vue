<template>
  <div class="row">
    <div class="col-sm-4"></div>
    <div class="col-sm-4">
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
          v-on:keyup.enter="submit"
        >
      </div>
      <div class="form-group">
        <input
          type="password"
          class="form-control"
          placeholder="Enter your password"
          v-model="credentials.password"
          v-on:keyup.enter="submit"
        >
      </div>
      <button class="login-btn btn" v-on:click="submit">Log in</button>
      <grid-loader v-if="loading" :loading="loading" :color="color" :size="size"></grid-loader>
    </div>
  </div>
</template>

<script>
  import auth from '../auth'
  import GridLoader from 'vue-spinner/src/GridLoader.vue'

  export default {
    data() {
      return {
        credentials: {
          username: '',
          password: ''
        },
        error: '',
        loading: false
      }
    },
    methods: {
      submit() {
        let credentials = {
          username: this.credentials.username,
          password: this.credentials.password
        };
        this.loading = true;
        auth.login(credentials, 'dashboard');
      }
    },
    components: {
        GridLoader
    }

  }
</script>

<style scoped>
  .login-btn {
    background-color: #41B883;
    color: #fff;
  }
</style>
