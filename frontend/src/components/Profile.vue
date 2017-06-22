<template>
  <div class="row">
    <div class="col-md-12">
      <h2>Profile page</h2>
      <p>Below you can find and edit your profile details as well as
        accept invitations you've received to existing projects</p>
      <hr class="small">
    </div>
    <div class="col-md-6">
      <div class="row">
        <div class="col-6 col-sm-3" style="text-align: left">
          <label for="username"><strong>Username:</strong></label>
        </div>
        <div class="col-6 col-sm-2">
          <div class="row">
            <div class="col-md-12 col-4" v-if="!allowEditUsername">
              <div class="icon-div" v-on:click="enableEditUsername(true)">
                <icon name="pencil-square-o"></icon>
              </div>
            </div>
            <div class="col-md-6 col-2" v-if="allowEditUsername && !usernameLoading">
              <div class="icon-div" v-on:click="editUsername">
                <icon id="submit" name="check-square-o"></icon>
              </div>
            </div>
            <div class="col-md-6 col-2" v-if="allowEditUsername && !usernameLoading">
              <div class="icon-div" v-on:click="enableEditUsername(false)">
                <icon id="cancel" name="window-close-o"></icon>
              </div>
            </div>
            <div class="col-md-12" v-if="usernameLoading">
              <pulse-loader class="loading" :loading="usernameLoading" :size="size"></pulse-loader>
            </div>
          </div>
        </div>
      </div>

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
      <div class="alert alert-danger" v-if="usernameError">
        <p>{{ usernameError }}</p>
      </div>
    </div>

    <div class="col-md-6">
      <div class="row">
        <div class="col-6 col-sm-3" style="text-align: left">
          <label for="password"><strong>Password:</strong></label>
        </div>
        <div class="col-6 col-sm-2">
          <div class="row">
            <div class="col-md-12 col-4" v-if="!allowEditPassword">
              <div class="icon-div" v-on:click="enableEditPassword(true)">
                <icon name="pencil-square-o"></icon>
              </div>
            </div>
            <div class="col-md-6 col-2" v-if="allowEditPassword && !passwordLoading">
              <div class="icon-div" v-on:click="editPassword">
                <icon id="submit" name="check-square-o"></icon>
              </div>
            </div>
            <div class="col-md-6 col-2" v-if="allowEditPassword && !passwordLoading">
              <div class="icon-div" v-on:click="enableEditPassword(false)">
                <icon id="cancel" name="window-close-o"></icon>
              </div>
            </div>
            <div class="col-md-12" v-if="passwordLoading">
              <pulse-loader class="loading" :loading="passwordLoading" :size="size"></pulse-loader>
            </div>
          </div>
        </div>
      </div>
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
          v-model="credentials.repeatPassword"
          v-on:keyup.enter="editPassword"
          disabled>
      </div>
      <div class="alert alert-danger" v-if="passwordError">
        <p>{{ passwordError }}</p>
      </div>
    </div>

    <project-invites v-bind:username="user.username"></project-invites>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  import axios from 'axios'
  import userService from '../store/user/userService'

  import ProjectInvites from './ProjectInvites.vue'

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
          repeatPassword: 'password'
        },
        allowEditUsername: false,
        allowEditPassword: false,
        usernameError: '',
        passwordError: '',
        size: '10px',
        usernameLoading: false,
        passwordLoading: false
      }
    },
    methods: {
      enableEditUsername (option) {
        document.getElementById('username').disabled = !option;
        this.allowEditUsername = option;
      },
      enableEditPassword (option) {
        document.getElementById('password').disabled = !option;
        document.getElementById('repeat-password').disabled = !option;
        if (option) {
          this.credentials.password = '';
          this.credentials.repeatPassword = '';
        } else {
          this.credentials.password = 'password';
          this.credentials.repeatPassword = 'password';
        }
        this.allowEditPassword = option;
      },
      editUsername () {
        if (this.user.username === this.credentials.username) {
          this.enableEditUsername(false);
          this.usernameError = '';
        } else {
          this.usernameLoading = true;
          axios.post(EDIT_USERNAME_URL,
            {username: this.credentials.username},
            userService.addAuthHeader()).then( response => {
            userService.refreshUser(response.data);
            this.enableEditUsername(false);
            this.usernameError = '';
            this.usernameLoading = false;
          }).catch( error => {
            this.usernameError = error.response.data.message;
            this.usernameLoading = false;
          })
        }
      },
      editPassword () {
        if (this.credentials.password === this.credentials.repeatPassword) {
          this.passwordLoading = true;
          axios.post(EDIT_PASSWORD_URL,
            {password: this.credentials.password, repeat_password: this.credentials.repeatPassword},
            userService.addAuthHeader()).then( () => {
            this.enableEditPassword(false);
            this.passwordError = '';
            this.passwordLoading = false;
          }).catch( error => {
            this.passwordLoading = false;
            this.passwordError = error.response.data.message
          })
        } else {
          this.passwordError = 'The passwords are not identical, please try again'
        }
      }
    },
    computed: {
      ...mapGetters({
        user: 'user'
      })

    },
    created () {
      this.credentials.username = this.user.username;
    },
    components: {
      Icon,
      PulseLoader,
      ProjectInvites
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
