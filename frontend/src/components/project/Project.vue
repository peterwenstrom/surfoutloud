<template>
  <div class="row">

    <div class="col-md-12">
      <h2>Project name: <i>{{project.name}}</i></h2>
      <p><strong>Project description: </strong><i>{{project.description}}</i></p>
      <hr class="small">
    </div>

    <member v-bind:username="user.username" v-bind:members="members"
            v-bind:activeMembers="activeMembers" @memberClick="openChat"></member>

    <div class="col-md-5 border-right">
      <h3>Chat</h3>

      <chat v-bind:projectId="project.id" v-bind:openChatRooms="openChatRooms"
            v-bind:chatArray="chatArray" v-bind:newDirectChat="newDirectChat"
            @activeUpdate="updateActiveMembers" @memberJoin="newMember" @closeRoom="closeChat"></chat>
    </div>

    <div class="col-md-5">
      <h3>Files</h3>
      <file v-bind:projectId="project.id"></file>
    </div>

  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  import axios from 'axios'
  import userService from '../../store/user/userService'

  import Member from './Member.vue'
  import Chat from './Chat.vue'
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
        openChatRooms: ['room'],
        chatArray:[
          {
            history: [
              { who: "", message: "" }
            ]
          }
        ],
        newDirectChat: ''
      }
    },
    methods: {
      updateActiveMembers (updatedActiveMembers) {
        this.activeMembers = updatedActiveMembers

      },
      getMembers() {
        axios.get(GET_MEMBERS_URL + this.project.id, userService.addAuthHeader()).then(response => {
          this.members = response.data.members;
        });
      },
      newMember (member){
        this.members.push(member);
      },
      openChat: function (member){
        // Open chat when member is pressed, change on variables will propagate to Chat.vue
        if (this.openChatRooms.indexOf(member) === -1) {
          this.openChatRooms.push(member);
          this.chatArray.push({history: [{ who: "", message: "" }]});
          this.newDirectChat = member
        }
      },
      closeChat: function(member){
        // Close chat is emitted from Chat.vue when user presses close button
        let index = this.openChatRooms.indexOf(member);
        this.chatArray.splice(index,1);
        this.openChatRooms.splice(index, 1);
        this.newDirectChat = ''
      }
    },
    components:{
      Member,
      Chat,
      File,
      Icon
    },
    computed: {
      ...mapGetters({
        project: 'project',
        projectSelected: 'projectSelected',
        user: 'user'
      })
    },
    created () {
      if (!this.projectSelected) {
        axios.get(GET_PROJECT_DETAILS_URL + this.$route.params.project_id, userService.addAuthHeader()).then(response => {
          this.$store.dispatch('setProjectObject', response.data.project);
          this.getMembers()
        })
      }
    },
    mounted (){
      if (this.projectSelected) {
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

  .border-right {
    border-right: 1px solid #eceeef;
  }

</style>
