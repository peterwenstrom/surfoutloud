<template>
  <div class="row">
    <div class="col-md-12">
      <h2>Profile page</h2>
      <p>Below you can find and edit your profile details</p>
      <hr class="small">
    </div>
    <div class="col-md-5">
      <div class="form-group">
        <input
          id="username"
          type="text"
          class="form-control profile-form"
          placeholder="Enter new username"
          v-model="credentials.username"
          v-on:keyup.enter="editUsername"
          disabled>
      </div>
      <div class="alert alert-danger" v-if="username_error">
        <p>{{ username_error }}</p>
      </div>
    </div>
    <div class="col-md-1">
      <div class="row">
        <div class="col-md-12" v-if="!edit_username">
          <div class="icon-div" v-on:click="enableEditUsername(true)">
            <icon name="pencil-square-o"></icon>
          </div>
        </div>
        <div class="col-md-6 col-2" v-if="edit_username && !username_loading">
          <div class="icon-div" v-on:click="editUsername">
            <icon id="submit" name="check-square-o"></icon>
          </div>
        </div>
        <div class="col-md-6 col-2" v-if="edit_username && !username_loading">
          <div class="icon-div" v-on:click="enableEditUsername(false)">
            <icon id="cancel" name="window-close-o"></icon>
          </div>
        </div>
        <div class="col-md-12" v-if="username_loading">
          <pulse-loader class="loading" :loading="username_loading" :size="size"></pulse-loader>
        </div>
      </div>
    </div>

    <div class="col-md-5">
      <div class="form-group">
        <input
          id="password"
          type="password"
          class="form-control profile-form"
          placeholder="Enter new password"
          v-model="credentials.password"
          v-on:keyup.enter="editPassword"
          disabled>
      </div>
      <div class="form-group">
        <input
          id="repeat-password"
          type="password"
          class="form-control profile-form"
          placeholder="Repeat new password"
          v-model="credentials.repeat_password"
          v-on:keyup.enter="editPassword"
          disabled>
      </div>
      <div class="alert alert-danger" v-if="password_error">
        <p>{{ password_error }}</p>
      </div>
    </div>
    <div class="col-md-1">
      <div class="row">
        <div class="col-md-12" v-if="!edit_password">
          <div class="icon-div" v-on:click="enableEditPassword(true)">
            <icon name="pencil-square-o"></icon>
          </div>
        </div>
        <div class="col-md-6 col-2" v-if="edit_password && !password_loading">
          <div class="icon-div" v-on:click="password_error='hejsan'">
            <icon id="submit" name="check-square-o"></icon>
          </div>
        </div>
        <div class="col-md-6 col-2" v-if="edit_password && !password_loading">
          <div class="icon-div" v-on:click="enableEditPassword(false)">
            <icon id="cancel" name="window-close-o"></icon>
          </div>
        </div>
        <div class="col-md-12" v-if="password_loading">
          <pulse-loader class="loading" :loading="password_loading" :size="size"></pulse-loader>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  import axios from 'axios'
  import userAuth from '../user/userAuth'

  import PulseLoader from 'vue-spinner/src/PulseLoader.vue'
  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/pencil-square-o'
  import 'vue-awesome/icons/check-square-o'
  import 'vue-awesome/icons/window-close-o'

  const EDIT_USERNAME_URL = API_URL + '/editusername';
  const EDIT_PASSWORD_URL = API_URL + '/editpassword';

  export default {
    data() {
      return {
        credentials: {
          username: '',
          password: 'password',
          repeat_password: 'password'
        },
        edit_username: false,
        edit_password: false,
        username_error: '',
        password_error: '',
        size: '10px',
        username_loading: false,
        password_loading: false
      }
    },
    methods: {
      enableEditUsername (option) {
        document.getElementById('username').disabled = !option;
        this.edit_username = option;
      },
      enableEditPassword (option) {
        document.getElementById('password').disabled = !option;
        document.getElementById('repeat-password').disabled = !option;
        if (option) {
          this.credentials.password = '';
          this.credentials.repeat_password = '';
        } else {
          this.credentials.password = 'password';
          this.credentials.repeat_password = 'password';
        }
        this.edit_password = option;
      },
      editUsername () {
        if (this.authUser.username === this.credentials.username) {
          this.enableEditUsername(false);
          this.username_error = '';
        } else {
          this.username_loading = true;
          axios.post(EDIT_USERNAME_URL,
            {username: this.credentials.username},
            userAuth.addAuthHeader()).then( response => {
            userAuth.refreshUser(response.data);
            this.enableEditUsername(false);
            this.username_error = '';
            this.username_loading = false;
          }).catch( error => {
            this.username_error = error.response.data.message;
            this.username_loading = false;
          })
        }
      },
      editPassword () {
        if (this.credentials.password === this.credentials.repeat_password) {
          this.password_loading = true;
          axios.post(EDIT_PASSWORD_URL,
            {password: this.credentials.password, repeat_password: this.credentials.repeat_password},
            userAuth.addAuthHeader()).then( () => {
            this.enableEditPassword(false);
            this.password_error = '';
            this.password_loading = false;
          }).catch( error => {
            this.password_loading = false;
            this.password_error = error.response.data.message
          })
        } else {
          this.password_error = 'The passwords are not identical, please try again'
        }
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
      Icon,
      PulseLoader
    }
  }

</script>

<style scoped>
  #submit {
    color: #41B883;
  }
  #cancel {
    color: #f44250;
  }
  .icon-div {
    display: inline;
  }
  .fa-icon {
    width: 20px;
    height: auto;
    padding-top: 5px;
    cursor: pointer;
  }
  .row {
    margin-top: 0px;
  }
  .loading {
    padding-top: 10px;
  }

</style>
