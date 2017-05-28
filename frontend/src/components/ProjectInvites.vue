<template>
  <div class="col-md-12">
    <hr class="small">
    <h3>Project Invites</h3>
    <transition-group name="fade">
      <div class="col-md-5 project" v-for="project in projects" v-bind:key="project">

        <div><p><strong>Project name:</strong> <br> {{project.name}}</p></div>
        <div><p><strong>Invited by:</strong> {{project.admin}}</p></div>
        <button class="btn btn-accept">Accept</button>
        <button class="btn btn-decline">Decline</button>

      </div>
    </transition-group>
  </div>
</template>

<script>
  import axios from 'axios'
  import authUser from '../user/userAuth'

  const GET_INVITES_URL = API_URL + '/getprojects/0';

  export default {
    data () {
      return {
        projects: []
      }
    },
    props: ['username'],
    created () {
      axios.get(GET_INVITES_URL, authUser.addAuthHeader()).then( response => {
        this.projects = response.data.projects;
        this.projects.forEach( project => {
          project['show'] = false
        })
      })
    }
  }
</script>

<style scoped>
  .project {
    display: inline-block;
    border: 1px solid #eceeef;
    border-radius: 25px;
    margin: 10px 10px 10px 10px;
    padding: 10px 0px 10px 0px;
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
</style>
