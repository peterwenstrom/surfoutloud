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
    </div>
  </div>
</template>

<script>
  import auth from '../auth'
  export default {
    data() {
      return {
        credentials: {
          username: '',
          password: ''
        },
        error: ''
      }
    },
    methods: {
      submit() {
        let credentials = {
          username: this.credentials.username,
          password: this.credentials.password
        };

        auth.login(credentials, 'dashboard');
      }
    }

  }
</script>

<style scoped>
  .login-btn {
    background-color: #41B883;
    color: #fff;
  }
</style>
