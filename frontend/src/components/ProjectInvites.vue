<template>
  <div class="col-md-12">
    <hr class="small">
    <h3>Project Invites</h3>
    <div v-for="project in projects">
      <p>{{project.name}}</p>
      <p>{{project.admin}}</p>
    </div>
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
      })
    }
  }
</script>

<style scoped>

</style>
