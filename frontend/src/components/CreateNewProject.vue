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
          required
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
          <p><strong>Select Project Icon</strong></p>
          <div class="project-icon">
            <label for="one"><icon name="superpowers"></icon></label>
            <input type="radio" id="one" value="superpowers" v-model="project_details.icon">
          </div>
          <div class="project-icon">
            <label for="two"><icon name="snowflake-o"></icon></label>
            <input type="radio" id="two" value="snowflake-o" v-model="project_details.icon">
          </div>
          <div class="project-icon">
            <label for="three"><icon name="anchor"></icon></label>
            <input type="radio" id="three" value="anchor" v-model="project_details.icon">
          </div>
          <div class="project-icon">
            <label for="four"><icon name="heart"></icon></label>
            <input type="radio" id="four" value="heart" v-model="project_details.icon">
          </div>
          <div class="project-icon">
            <label for="five"><icon name="diamond"></icon></label>
            <input type="radio" id="five" value="diamond" v-model="project_details.icon">
          </div>
          <div class="project-icon">
            <label for="six"><icon name="hand-spock-o"></icon></label>
            <input type="radio" id="six" value="hand-spock-o" v-model="project_details.icon">
          </div>
          <div class="project-icon">
            <label for="seven"><icon name="star"></icon></label>
            <input type="radio" id="seven" value="star" v-model="project_details.icon">
          </div>
          <div class="project-icon">
            <label for="eight"><icon name="paw"></icon></label>
            <input type="radio" id="eight" value="paw" v-model="project_details.icon">
          </div>
          <div class="project-icon">
            <label for="nine"><icon name="glass"></icon></label>
            <input type="radio" id="nine" value="glass" v-model="project_details.icon">
          </div>
          <div class="project-icon">
            <label for="ten"><icon name="globe"></icon></label>
            <input type="radio" id="ten" value="globe" v-model="project_details.icon">
          </div>
          <hr class="small">
        </div>


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
            <icon id="add-member" name="plus-circle"></icon>
          </div>
        </div>
        <div class="col-md-12">
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
      <pulse-loader :loading="loading" ></pulse-loader>
      <button class="create-btn btn" v-if="!loading" v-on:click="createProject">Create project</button>
      <div class="alert alert-danger" v-if="error">
        <p>{{ error }}</p>
      </div>
    </div>
  </div>

</template>

<script>
  import axios from 'axios'
  import { mapGetters } from 'vuex'
  import userAuth from '../user/userAuth'

  import PulseLoader from 'vue-spinner/src/PulseLoader.vue'
  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/plus-circle'
  import 'vue-awesome/icons/window-close-o'
  import 'vue-awesome/icons/superpowers'
  import 'vue-awesome/icons/snowflake-o'
  import 'vue-awesome/icons/anchor'
  import 'vue-awesome/icons/heart'
  import 'vue-awesome/icons/diamond'
  import 'vue-awesome/icons/hand-spock-o'
  import 'vue-awesome/icons/globe'
  import 'vue-awesome/icons/star'
  import 'vue-awesome/icons/paw'
  import 'vue-awesome/icons/glass'

  const ADD_PROJECT_URL = API_URL + '/addproject';

  export default {
    name: 'CreateNewProject',
    data() {
      return {
        project_details: {
          new_members: [],
          name: '',
          description: '',
          admin: '',
          icon: 'superpowers'
        },
        msg: '',
        member: '',
        error: '',
        loading: false
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
        this.loading = true;
        axios.post(ADD_PROJECT_URL, this.project_details, userAuth.addAuthHeader()).then( response => {
          this.loading = false;
          this.$router.push('project?attr=' + response.data.project_id)
        }).catch( error => {
          this.loading = false;
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
      Icon,
      PulseLoader
    }
  };


</script>

<style scoped>
  .create-btn {
    background-color: #41B883;
    color: #fff;
    cursor: pointer;
  }
  .alert {
    margin-top: 20px;
  }
  .fa-icon {
    color: #2973b7;
    cursor: pointer;
    width: 25px;
    height: auto;
  }
  .icon-div {
    display: inline-block;
    vertical-align: middle;
  }
  #add-member {
    color: #41B883;
    width: 20px;
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
    color: #f66;
    width: 20px;
    padding-left: 5px;
  }
  .project-icon {
    display: inline-block;
    margin: 0px 5px 0px 5px;
  }
  .project-icon label {
    display: block;
    margin-bottom: 0;
  }
  .project-icon input {
    cursor: pointer;
  }
  #project-description, #add-members {
    margin-bottom: 16px;
  }

</style>


