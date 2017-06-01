<template>
  <div class="hello row">
    <div class="col-md-12">
      <h2>Project name: <i>{{project.name}}</i></h2>
      <p><strong>Project description: </strong><i>{{project.description}}</i></p>
      <hr class="small">
    </div>
    <div class="col-md-2 border-right">
      <h3>Members</h3>
      <hr class="small">
      <table class="table table-striped">
        <tbody>
        <tr v-for="(member,index) in members">
          <td>
            <p v-if="member !== authUser.username" v-on:click="openChat(member)" class="point">{{ member }}</p>
            <p v-else>{{ member }}</p>

          </td>
          <td>
            <icon v-if="ifUserIsActive(member)" class="green" name="user"></icon>
            <icon v-else name="user"></icon>

            <!--<div v-if="ifUserIsOpen(member)" v-on:click="closeChat(member)">
              <icon name="minus" class="point"></icon>
            </div>-->
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <div class="col-md-5 border-right">
      <h3>Chat</h3>

      <chat v-bind:projectId="project.id" v-bind:openChatRooms="openChatRooms" v-bind:chatArray="chatArray" @active="updateActiveMembers" @member_join="newMember" @closeRoom="closeChat"></chat>
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
  import userAuth from '../user/userAuth'

  import Chat from './Chat'
  import File from './File'

  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/user'
  import 'vue-awesome/icons/minus'

  const GET_MEMBERS_URL = API_URL + '/getmembers/';
  const GET_PROJECT_DETAILS_URL = API_URL + '/getprojectdetails/';

  export default {
    name: 'project',
    data () {
      return {
        members: [],
        activeMembers: [],
        isActive: false,
        openChatRooms: ['room'],
        chatArray:[
          {
            history: [
              { who: "", message: "" }
            ]
          }
        ],
      }
    },
    methods: {
      updateActiveMembers (updatedActiveMembers) {
        this.activeMembers = updatedActiveMembers

      },
      ifUserIsActive (user) {
        if (this.activeMembers.indexOf(user) > -1) {
          return true;
        } else {
          return false;
        }

      },
      ifUserIsOpen (user) {
        if (this.openChatRooms.indexOf(user) > -1) {
          return true;
        } else {
          return false;
        }

      },
      getMembers() {
        axios.get(GET_MEMBERS_URL + this.project.id, userAuth.addAuthHeader()).then( response => {
          this.members = response.data.members;
        });
      },
      newMember (member){
        this.members.push(member);
      },
      openChat: function (member){

        if (this.openChatRooms.indexOf(member) === -1) {
          this.openChatRooms.push(member);
          this.chatArray.push({history: [{ who: "", message: "" }]});
        }
      },
      closeChat: function(member){

        let index = this.openChatRooms.indexOf(member);


        this.chatArray.splice(index,1);



        this.openChatRooms.splice(index, 1);

      }
    },
    components:{
      Chat,
      Icon,
      File
    },
    computed: {
      ...mapGetters({
        project: 'project',
        project_selected: 'project_selected',
        authUser: 'authUser'
      })
    },
    created () {
      if (!this.project_selected) {
        axios.get(GET_PROJECT_DETAILS_URL + this.$route.params.project_id, userAuth.addAuthHeader()).then( response => {
          this.$store.dispatch('setProjectObject', response.data.project);
          this.getMembers()
        })
      }
    },
    mounted (){
      if (this.project_selected) {
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

  a {
    color: #42b983;
  }
  td p {
    text-align: left;
  }
  td * {
    vertical-align: middle;
    margin-top: 0;
    margin-bottom: 0;
  }
  .green {
    color: #41B883;
  }
  .border-right {
    border-right: 1px solid #eceeef;
  }
  .point {
    cursor: pointer;
  }

</style>
