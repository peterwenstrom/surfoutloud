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
        <tr v-for="(item, index) in memberList">
          <td>
            <p>{{ item }}</p>
          </td>
          <td>
            <icon v-if="activeUserList[index] === 'true'" class="green" name="user"></icon>
            <icon v-else name="user"></icon>
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <div class="col-md-6 border-right">
      <h3>Chat</h3>

      <chat v-bind:projectId="project.id" @active="onActiveUserUpdate"></chat>
    </div>
    <div class="col-md-4">
      <h3>Files</h3>
      <file v-bind:projectId="project.id"></file>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue'
  import {mapGetters} from 'vuex'
  import axios from 'axios'
  import userAuth from '../user/userAuth'

  import Chat from './Chat'
  import File from './File'

  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/user'

  const GET_MEMBERS_URL = API_URL + '/getmembers/';
  const GET_PROJECT_DETAILS_URL = API_URL + '/getprojectdetails/';

  export default {
    name: 'project',
    data () {
      return {
        memberList: [

        ],
        activeUserList: [

        ],
        isActive: false
      }
    },
    methods: {
      onActiveUserUpdate (value) {
        let i = 0;

        for (i; i<this.memberList.length; i++){

          if (value.indexOf(this.memberList[i]) > -1 ){
            this.activeUserList.splice(i, 1, 'true');

          } else {
            this.activeUserList.splice(i, 1, 'false');
          }
        }

      },
      getMembers() {
        axios.get(GET_MEMBERS_URL + this.project.id, userAuth.addAuthHeader()).then( response => {
          let i = 0;

          for (i; i<response.data.members.length; i++){
            //the drawback here is that you cannot have usernames with space in it.. maybe we do not want it anyway
            Vue.set(this.memberList, i, JSON.stringify(response.data.members[i]).replace(/[^a-zA-Z]+/g, ''));
          }
        });
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
        project_selected: 'project_selected'
      })
    },
    created () {
      if (!this.project_selected) {
        axios.get(GET_PROJECT_DETAILS_URL + this.$route.params.project_id, userAuth.addAuthHeader()).then( response => {
          this.$store.dispatch('setProjectObject', response.data.project);
          this.getMembers();
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
  .green {
    color: #41B883;
  }
  .border-right {
    border-right: 1px solid #eceeef;
  }

</style>
