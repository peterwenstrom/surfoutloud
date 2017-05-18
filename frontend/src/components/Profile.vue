<template>
  <div class="row">
    <div class="col-md-12">
      <h2>Profile page</h2>
      <p>Below you can find and edit your profile details</p>
    </div>
    <div class="col-md-5">
      <div class="form-group">
        <input
          id="username"
          type="text"
          class="form-control profile-form"
          placeholder="Enter new username"
          v-model="credentials.username"
          v-on:keyup.enter=""
          disabled>
      </div>
      <div class="alert alert-danger" v-if="username_error">
        <p>{{ username_error }}</p>
      </div>
    </div>
    <div class="col-md-1">
      <div class="row">
        <div class="col-md-12" v-if="!edit_username">
          <div class="icon-div" v-on:click="editUsername(true)">
            <icon name="pencil-square-o"></icon>
          </div>
        </div>
        <div class="col-md-6 col-2" v-if="edit_username">
          <div class="icon-div" v-on:click="username_error='hejsan'">
            <icon id="submit" name="check-square-o"></icon>
          </div>
        </div>
        <div class="col-md-6 col-2" v-if="edit_username">
          <div class="icon-div" v-on:click="editUsername(false)">
            <icon id="cancel" name="window-close-o"></icon>
          </div>
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
          v-on:keyup.enter=""
          disabled>
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
      <div class="alert alert-danger" v-if="password_error">
        <p>{{ password_error }}</p>
      </div>
    </div>
    <div class="col-md-1">
      <div class="row">
        <div class="col-md-12" v-if="!edit_password">
          <div class="icon-div" v-on:click="editPassword(true)">
            <icon name="pencil-square-o"></icon>
          </div>
        </div>
        <div class="col-md-6 col-2" v-if="edit_password">
          <div class="icon-div" v-on:click="password_error='hejsan'">
            <icon id="submit" name="check-square-o"></icon>
          </div>
        </div>
        <div class="col-md-6 col-2" v-if="edit_password">
          <div class="icon-div" v-on:click="editPassword(false)">
            <icon id="cancel" name="window-close-o"></icon>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'

  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/pencil-square-o'
  import 'vue-awesome/icons/check-square-o'
  import 'vue-awesome/icons/window-close-o'

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
        password_error: ''
      }
    },
    methods: {
      editUsername (option) {
        document.getElementById('username').disabled = !option;
        this.edit_username = option;
      },
      editPassword (option) {
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

</style>
