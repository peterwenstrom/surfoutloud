<template>

  <div class="row">
    <div class="col-md-12">
      <h2>Create New Project</h2>
      <p>Create a new project and add members to it</p>
      <hr class="small">
    </div>
    <div class="col-md-6">
      <label for="project-name"><strong>Project Name:</strong></label>
      <div class="form-group">
        <input
          id="project-name"
          type="text"
          class="form-control"
          placeholder="Add a name to your project"
          v-model="projectDetails.name"
          required
        >
      </div>
      <label for="project-description"><strong>Project Description:</strong></label>

      <textarea
        id="project-description"
        rows="5"
        class="form-control"
        placeholder="Add a short description of your project"
        v-model="projectDetails.description"
        v-on:keyup.enter=""
      ></textarea>
      <div class="col-md-12">
        <label for="add-members"><strong>Add Members:</strong></label>
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
      <div class="added-member" v-for="member in projectDetails.members">

        <a>{{ member }}</a>
        <div class="icon-div" v-on:click="removeMember(member)">
          <icon id="cancel" name="window-close-o"></icon>
        </div>
      </div>
    </div>

    <div class="col-md-6">
      <div class="row">
        <div class="col-md-12">
          <p><strong>Select Project Icon:</strong></p>

          <div class="project-icon" v-for="icon in icons">
            <label v-bind:for="icon">
              <icon v-bind:style="{color: projectDetails.color}" v-bind:name="icon"></icon>
            </label>
            <input type="radio" v-bind:id="icon" v-bind:value="icon" v-model="projectDetails.icon">
          </div>

          <hr class="small">
        </div>

        <div class="col-md-12">
          <p><strong>Select Project Color Theme:</strong></p>
          <swatches class="color-picker" v-model="colors" @input="updateSelectedColor"></swatches>
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
  import userService from '../../store/user/userService'

  import PulseLoader from 'vue-spinner/src/PulseLoader.vue'
  import { Swatches } from 'vue-color'
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
        projectDetails: {
          members: [],
          name: '',
          description: '',
          admin: '',
          icon: 'superpowers',
          color: '#0D47A1'
        },
        member: '',
        colors: {hex: '#0D47A1'},
        icons: ['superpowers', 'snowflake-o', 'anchor', 'heart', 'diamond',
                'hand-spock-o', 'globe', 'star', 'paw', 'glass'],
        error: '',
        loading: false
      }
    },
    methods: {
      addMember () {
        if (this.member !== '') {
          this.projectDetails.members.push(this.member);
          this.member = '';
        }
      },
      removeMember (user) {
        const index = this.projectDetails.members.indexOf(user);
        if (index > -1) {
          this.projectDetails.members.splice(index, 1);
        }
      },
      createProject () {
        this.loading = true;
        let project_details = this.projectDetails;
        axios.post(ADD_PROJECT_URL, project_details, userService.addAuthHeader()).then(response => {
          this.loading = false;
          this.$store.dispatch('setProjectObject', response.data);
          this.$router.push('project/' + response.data.id)
        }).catch( error => {
          this.loading = false;
          this.error = error.response.data.message
        })
      },
      updateSelectedColor(newColor) {
        this.projectDetails.color = newColor.hex
      }
    },
    computed: {
      ...mapGetters({
        user: 'user'
      })
    },
    mounted () {
      this.projectDetails.admin = this.user.username
    },
    components: {
      Icon,
      PulseLoader,
      Swatches
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
    display: inline-block;
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
  .color-picker {
    width: 100%;
    height: 292px;
  }

</style>


