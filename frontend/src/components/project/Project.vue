<template>
  <div>
    <div class="alert alert-danger" v-if="error">
      <h2>{{error}}</h2>
    </div>
    <div class="row" v-if="!error">

      <div class="col-md-12">
        <h2>Project name: <i>{{project.name}}</i></h2>
        <p><strong>Project description: </strong><i>{{project.description}}</i></p>
        <hr class="small">
      </div>

      <member v-bind:username="user.username" v-bind:members="members"
              v-bind:activeMembers="activeMembers" @memberClick="openChat"></member>

      <chat v-bind:projectId="project.id" v-bind:user="user" v-bind:members="members"
            v-bind:openRooms="openRooms" @closeRoom="closeRoom"
            @activeUpdate="updateActiveMembers" @memberJoin="newMember" ></chat>

      <div class="col-md-5">
        <h3>Files</h3>
        <file v-bind:projectId="project.id"></file>
      </div>

    </div>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  import axios from 'axios'
  import userService from '../../store/user/userService'

  import Member from './Member.vue'
  import Chat from './chat/Chat.vue'
  import File from './File.vue'

  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/minus'

  const GET_MEMBERS_URL = API_URL + '/getmembers/';
  const GET_PROJECT_DETAILS_URL = API_URL + '/getprojectdetails/';

  export default {
    name: 'project',
    data () {
      return {
        members: [],
        activeMembers: [],
        openRooms: [],
        error: ''
      }
    },
    computed: {
      ...mapGetters({
        project: 'project',
        projectSelected: 'projectSelected',
        user: 'user'
      })
    },
    methods: {
      updateActiveMembers (updatedActiveMembers) {
        this.activeMembers = updatedActiveMembers

      },
      getMembers() {
        axios.get(GET_MEMBERS_URL + this.project.id, userService.addAuthHeader()).then(response => {
          this.members = response.data.members;
        }).catch(error => {
          if (error.response) {
            this.error = error.response.data.message
          } else {
            this.error = 'Error when retrieving project members, please try again'
          }
        })
      },
      newMember (member){
        this.members.push(member);
      },
      openChat: function (member){
        // Open chat when member is pressed, change on variables will propagate to Chat.vue
        if (this.openRooms.indexOf(member) === -1) {
          this.openRooms.push(member);
        }
      },
      closeRoom: function(member){
        // Close chat is emitted from Chat.vue when user presses close button
        let index = this.openRooms.indexOf(member);
        this.openRooms.splice(index, 1);
      }
    },
    components:{
      Member,
      Chat,
      File,
      Icon
    },
    created () {
      if (!this.projectSelected) {
        axios.get(GET_PROJECT_DETAILS_URL + this.$route.params.project_id, userService.addAuthHeader()).then(response => {
          this.$store.dispatch('setProjectObject', response.data.project);
          this.getMembers()
        }).catch(error => {
          if (error.response) {
            this.error = error.response.data.message
          } else {
            this.error = 'Error when retrieving project details, please try again'
          }
        })
      } else {
        this.getMembers()
      }
    },
    beforeDestroy() {
      this.$store.dispatch('clearProjectObject')
    }
  }
</script>

<style scoped>
  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

</style>
