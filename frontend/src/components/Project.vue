<template>
  <div class="hello row">
    <div class="col-md-2">
      <h2>Members</h2>
      <table class="table table-striped">
        <tbody>
        <tr v-for="(item, index) in memberList">
          <td>
            <p>{{ item }}</p>
            <icon v-if="activeUserList[index] === 'true'" class="green" name="user"></icon>
            <icon v-else name="user"></icon>
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <div class="col-md-6">
      <h2>Chat</h2>
      <chat v-bind:projectId="project.id" @active="onActiveUserUpdate"></chat>
    </div>
    <div class="col-md-4">
      <h2>Files</h2>
      <file></file>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue'
  import {mapGetters} from 'vuex'
  import axios from 'axios'
  import Chat from './Chat'
  import File from './File'


  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/user'

  const GET_MEMBERS_URL = API_URL + '/getmembers';

  export default {
    name: 'project',
    data () {
      return {
        memberList: [

        ],
        activeUserList: [

        ],
        isActive: false,
        projectId: ""
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

      }
    },
    components:{
      Chat,
      Icon,
      File
    },
    computed: {
      ...mapGetters({
        project: 'project'
      })
    },
    created() {
      this.projectId = this.project.id
    },
    mounted(){

      axios.post(GET_MEMBERS_URL, {project_id: this.project.id}).then( response => {
        let i = 0;

        for (i; i<response.data.members.length; i++){
          //the drawback here is that you cannot have usernames with space in it.. maybe we do not want it anyway
          Vue.set(this.memberList, i, JSON.stringify(response.data.members[i]).replace(/[^a-zA-Z]+/g, ''));
        }
      });
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
  p {
    margin-right: 5px;
    display: inline-block;
  }
  .green {
    color: #41B883;
  }

</style>
