<template>

  <div class="row">
    <div class="col-lg-12 text-center">
      <h2>Dashboard</h2>
      <hr class="small">
      <div class="row">
        <div class="col-md-3 col-sm-6">
          <div class="portfolio-item">
            <router-link to="/CreateNewProject">
              <p>Create new project</p>
              <icon name="plus-circle"></icon>
            </router-link>
          </div>
        </div>
        <div class="col-md-3 col-sm-6">
          <div class="portfolio-item">
            <router-link to="/project">
              <p>Project 1</p>
              <img class="img-portfolio img-responsive project" src="../assets/portfolio-2.jpg">
            </router-link>
          </div>
        </div>
        <div v-for="project in projects" class="col-md-3 col-sm-6">
          <project-widget v-bind:project="project"></project-widget>
        </div>
      </div>
    </div>
  </div>



</template>

<script>
  import 'vue-awesome/icons/plus-circle'
  import Icon from 'vue-awesome/components/Icon'
  import ProjectWidget from './ProjectWidget.vue'
  import axios from 'axios'
  import {mapGetters} from 'vuex'

  export default {
    name: 'Dashboard',
    data() {
      return {
        projects: []
      }
    },
    computed: {
      ...mapGetters({
        authUser: 'authUser'
      })
    },
    methods: {
    },
    components: {
      Icon,
      ProjectWidget
    },
    mounted () {
      axios.get('/api/getprojects',
        {headers: {'Authorization': 'Bearer ' + this.authUser.access_token}}).then( response => {
        console.log(response);
        this.projects = response.data.projects;
      });
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

  .project {
    width: 80%;
    height: 80%;
  }

  .fa-icon {
    width: 48%;
    height: auto;
  }

</style>
