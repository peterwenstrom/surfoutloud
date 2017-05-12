<template>

  <div class="row">
    <div class="col-lg-12 text-center">
      <h2>Dashboard</h2>
      <hr class="small">
      <div v-if="!loading" class="row">
        <div class="col-md-3 col-sm-6">
          <div class="portfolio-item">
            <router-link to="/createnewproject">
              <p>Create new project</p>
              <icon name="plus-circle"></icon>
            </router-link>
          </div>
        </div>

        <div v-for="project in projects" class="col-md-3 col-sm-6">
          <project-widget v-bind:project="project"></project-widget>
        </div>
      </div>
      <ring-loader class="loading" v-if="loading" :loading="loading" :color="color" :size="size"></ring-loader>
    </div>
  </div>



</template>

<script>
  import axios from 'axios'
  import {mapGetters} from 'vuex'
  import userAuth from '../user/userAuth'

  import ProjectWidget from './ProjectWidget.vue'
  import RingLoader from 'vue-spinner/src/RingLoader.vue'
  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/plus-circle'

  export default {
    name: 'Dashboard',
    data() {
      return {
        projects: [],
        loading: false,
        color: '#41B883',
        size: '120px',
        margin: '2px',
        radius: '2px'
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
      ProjectWidget,
      RingLoader
    },
    mounted () {
      this.loading = true;
      setTimeout(() => {
        axios.get('/api/getprojects', userAuth.addAuthHeader() ).then( response => {
          this.projects = response.data.projects;
          this.loading = false;
        });
      }, 1000);
    }
  };


</script>

<style scoped>

  .fa-icon {
    width: 48%;
    height: auto;
  }
  .loading {
    text-align:center;
    display: inline-block;
  }

</style>
