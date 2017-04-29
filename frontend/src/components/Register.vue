<template>
  <div class="col-sm-4 col-sm-offset-4">
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
        }

        auth.register(credentials, 'dashboard')
      }
    }

  }
</script>

<style scoped>
  .register-btn {
    background-color: #35495E;
    color: #fff;
  }
</style>
