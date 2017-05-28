<template>
  <div class="col-md-12">
    <hr class="small">
    <h3>Project Invites</h3>
    <div class="alert alert-danger" v-if="error">
      <p>{{ error }}</p>
    </div>
    <transition-group name="fade">
      <div class="col-md-5 project" v-for="(project, index) in projects" v-bind:key="project">
        <div v-if="response_index !== index">
          <div><p><strong>Project name:</strong> <br> {{project.name}}</p></div>
          <div><p><strong>Invited by:</strong> {{project.admin}}</p></div>
          <button class="btn btn-accept" v-on:click="answerInvite(project.id, 'accept', index)">Accept</button>
          <button class="btn btn-decline" v-on:click="answerInvite(project.id, 'decline', index)">Decline</button>
        </div>
        <div class="alert alert-success alert-response" v-if="response_index === index">
          <p>{{ response_message }}</p>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script>
  import axios from 'axios'
  import authUser from '../user/userAuth'

  const GET_INVITES_URL = API_URL + '/getprojects/0';
  const ANSWER_INVITE_URL = API_URL + '/answerprojectinvite';

  export default {
    data () {
      return {
        projects: [],
        response_index: '',
        response_message: '',
        error: ''
      }
    },
    props: ['username'],
    created () {
      axios.get(GET_INVITES_URL, authUser.addAuthHeader()).then( response => {
        this.projects = response.data.projects
      })
    },
    methods: {
      answerInvite (id, answer, index) {
        let answer_object = {
          project_id: id,
          answer: answer
        };
        axios.post(ANSWER_INVITE_URL, answer_object, authUser.addAuthHeader()).then( response => {
          this.response_message = response.data.message;
          this.response_index = index;
          setTimeout( () => {
            this.response_message = '';
            this.response_index = '';
            this.projects.splice(index, 1)
          }, 1600)
        }).catch( error => {
          if (error.response) {
            this.error = error.response.data.message
          } else {
            this.error = 'Something went wrong, please check your connection and try again.'
          }
        })
      }
    }
  }
</script>

<style scoped>
  .project {
    display: inline-block;
    border: 1px solid #eceeef;
    border-radius: 25px;
    margin: 10px 10px 10px 10px;
    padding: 10px 3px 10px 3px;
  }
  .btn-accept {
    background-color: #41B883;
    color: #fff;
    margin-right: 15px;
    cursor: pointer;
  }
  .btn-decline {
    background-color: #f44250;
    color: #fff;
    cursor: pointer;
  }
  p {
    display: inline-block;
  }
  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s
  }
  .fade-enter, .fade-leave-to {
    opacity: 0
  }
  .alert-response {
    margin-bottom: 0;
    border-radius: 10px;
  }
  .alert-response p {
    margin-top: 0;
    margin-bottom: 0;
  }
</style>
