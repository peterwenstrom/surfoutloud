<template>

  <div>
    <h1>Create New Project</h1>

    <div class="col-md-12">
      <input v-model="member" v-on:keyup.enter="addMember"/>
      <button class="send-btn btn" v-on:click="addMember">Add member</button>
    </div>
    <p v-model="msg"></p>
    <h6>Members to be added in this project:</h6>
    <p>{{ newMember.username }}</p>


    <button class="send-btn btn" v-on:click="createProject">Create project</button>
  </div>

</template>

<script>
  import axios from 'axios';
  import {mapGetters} from 'vuex';
  const API_URL = 'http://localhost:5000/';
  const ADDPROJECT_URL = API_URL + 'addproject';

  export default {
    name: 'CreateNewProject',
    data() {
      return {
        newMember: {
          username: []
        },
        msg: "",
        member:""
      }
    },
    methods: {
              addMember: function() {
                this.newMember.username.push(this.member);
                this.member = "";
              },
              createProject: function() {
                  let adminAndMembers = {
                  username: this.authUser.username,
                    memberArray: this.newMember.username
                  };
                axios.post(ADDPROJECT_URL, adminAndMembers).then(response => {
                    this.$router.push('dashboard');
                }).catch(err => {
                    //Todo: error handling when user put in members not in db
                    this.msg = err.response.data.msg;

                })
              }
            },
    computed: {
      ...mapGetters({
        authUser: 'authUser'
      })
    }
  };


</script>

<style>
  .row {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }

</style>


