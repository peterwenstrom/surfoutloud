<template>
  <div class="row">
    <div class="col-md-12">
      <h2>Profile page</h2>
      <p>Below you can find and edit your profile details</p>
    </div>
    <div class="col-md-6">
      <div class="form-group">
        <input
          id="username"
          type="text"
          class="form-control profile-form"
          placeholder="Enter new username"
          v-model="credentials.username"
          v-on:keyup.enter=""
          disabled>
        <div class="edit" v-on:click="unlockUsername"><icon name="pencil-square-o"></icon></div>
      </div>
    </div>
    <div class="col-md-6">
      <div class="alert alert-danger" v-if="error">
        <p>{{ error }}</p>
      </div>
      <div class="form-group">
        <input
          id="password"
          type="password"
          class="form-control profile-form"
          placeholder="Enter new password"
          v-model="credentials.password"
          v-on:keyup.enter=""
          disabled>
        <div class="edit" v-on:click="unlockPassword"><icon name="pencil-square-o"></icon></div>
      </div>
      <div class="form-group">
        <input
          id="repeat-password"
          type="password"
          class="form-control profile-form"
          placeholder="Repeat new password"
          v-model="credentials.repeat_password"
          v-on:keyup.enter=""
          disabled>
      </div>
      <button class="register-btn btn" v-on:click="">Register</button>
    </div>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'

  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/pencil-square-o'

  export default {
    data() {
      return {
        credentials: {
          username: '',
          password: 'password',
          repeat_password: 'password'
        },
        error: ''
      }
    },
    methods: {
      unlockUsername () {
        document.getElementById('username').disabled = false;

      },
      unlockPassword () {
        document.getElementById('password').disabled = false;
        document.getElementById('repeat-password').disabled = false;
        this.credentials.password = '';
        this.credentials.repeat_password = '';
      }
    },
    computed: {
      ...mapGetters({
        authUser: 'authUser'
      })
    },
    created () {
        this.credentials.username = this.authUser.username;
    },
    components: {
      Icon
    }
  }

</script>

<style scoped>
  .edit {
    display: inline-block;
    cursor: pointer;
    padding-left: 5px;
  }
  .profile-form {
    display:inline-block;
    width:80%;
  }

</style>
