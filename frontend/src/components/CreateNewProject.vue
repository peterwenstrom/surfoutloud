<template>

  <div class="row">
    <div class="col-md-12">
      <h2>Create New Project</h2>
      <p>Create a new project and add members to it</p>
      <hr class="small">
    </div>
    <div class="col-md-6">
      <label for="project-name"><strong>Project Name</strong></label>
      <div class="form-group">
        <input
          id="project-name"
          type="text"
          class="form-control"
          placeholder="Add a name to your project"
          v-model="project_name"
          v-on:keyup.enter=""
        >
      </div>
      <label for="project-description"><strong>Project Description</strong></label>
      <div class="form-group">
        <input
          id="project-description"
          type="text"
          class="form-control"
          placeholder="Add a short description of your project"
          v-model="project_description"
          v-on:keyup.enter=""
        >
      </div>
    </div>

    <div class="col-md-6">
      <div class="row">
        <div class="col-md-12">
          <label for="add-members"><strong>Add Members</strong></label>
          <input
            id="add-members"
            type="text"
            class="form-control"
            v-model="member"
            v-on:keyup.enter="addMember"
          >

          <div class="icon-div" v-on:click="addMember">
            <icon name="plus-circle"></icon>
          </div>
        </div>
        <div class="col-md-12">
          <hr class="small">
          <p><strong>Members that will be added to the project:</strong></p>
        </div>
        <div class="added-member" v-for="member in newMember.username">

          <a>{{ member }}</a>
          <div class="icon-div" v-on:click="removeMember(member)">
            <icon id="cancel" name="window-close-o"></icon>
          </div>
        </div>
      </div>
    </div>


    <div class="col-md-12">
      <hr class="small">
      <button class="create-btn btn" v-on:click="createProject">Create project</button>
    </div>
  </div>

</template>

<script>
  import axios from 'axios'
  import { mapGetters } from 'vuex'
  import userAuth from '../user/userAuth'

  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/plus-circle'

  const ADDPROJECT_URL = API_URL + '/addproject';

  export default {
    name: 'CreateNewProject',
    data() {
      return {
        newMember: {
          username: []
        },
        project_name: '',
        project_description: '',
        msg: '',
        member: '',
        error: ''
      }
    },
    methods: {
      addMember () {
        this.newMember.username.push(this.member);
        this.member = "";
      },
      removeMember (user) {
        const index = this.newMember.username.indexOf(user);
        if (index > -1) {
          this.newMember.username.splice(index, 1);
        }
      },
      createProject () {
        let adminAndMembers = {
          username: this.authUser.username,
          memberArray: this.newMember.username
        };
        axios.post(ADDPROJECT_URL, adminAndMembers, userAuth.addAuthHeader()).then( response => {
          this.$router.push('dashboard')
        }).catch( error => {
          this.error = error.response.data.message
        })
      }
    },
    computed: {
      ...mapGetters({
        authUser: 'authUser'
      })
    },
    components: {
      Icon
    }
  };


</script>

<style scoped>
  .create-btn {
    background-color: #41B883;
    color: #fff;
    cursor: pointer;
  }
  .fa-icon {
    color: #41B883;
    cursor: pointer;
    width: 20px;
    height: auto;
  }
  .icon-div {
    display: inline-block;
    vertical-align: middle;
  }
  #add-members {
    display: inline-block;
    width: 50%;
  }
  .added-member {
    border: 1px solid #c6c6c6;
    border-radius: 5px;
    margin: 5px 5px 5px 5px;
    padding: 0px 10px 0px 10px;
    text-align: left;
  }
  #cancel {
    color: #f44250;
    padding-left: 5px;
  }

</style>


