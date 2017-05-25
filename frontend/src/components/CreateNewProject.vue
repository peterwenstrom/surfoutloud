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
          v-model="project_details.name"
          v-on:keyup.enter=""
        >
      </div>
      <label for="project-description"><strong>Project Description</strong></label>

      <textarea
        id="project-description"
        rows="5"
        class="form-control"
        placeholder="Add a short description of your project"
        v-model="project_details.description"
        v-on:keyup.enter=""
      ></textarea>

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
        <div class="added-member" v-for="member in project_details.new_members">

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
        project_details: {
          new_members: [],
          name: '',
          description: '',
          admin: ''
        },
        msg: '',
        member: '',
        error: ''
      }
    },
    methods: {
      addMember () {
        this.project_details.new_members.push(this.member);
        this.member = "";
      },
      removeMember (user) {
        const index = this.project_details.new_members.indexOf(user);
        if (index > -1) {
          this.project_details.new_members.splice(index, 1);
        }
      },
      createProject () {
        axios.post(ADDPROJECT_URL, this.project_details, userAuth.addAuthHeader()).then( response => {
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
    mounted () {
      this.project_details.admin = this.authUser.username
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


