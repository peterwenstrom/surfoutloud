<template>

  <div class="row">
    <div class="col-lg-12 text-center">
      <h2>Dashboard</h2>
      <hr class="small">
      <div v-if="!loading" class="row">
        <div class="col-lg-3 col-md-4 col-sm-6">
          <div id="create-widget">
            <router-link class="create" to="/createnewproject">
              <p><strong>Create new project</strong></p>
              <icon name="plus-circle"></icon>
            </router-link>
          </div>
        </div>

        <div v-for="project in projects" class="col-lg-3 col-md-4 col-sm-6">
          <project-widget v-bind:project="project" v-bind:widgetHeight="widgetHeight"></project-widget>
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

  const GET_PROJECT_URL = API_URL + '/getprojects/1';

  export default {
    name: 'Dashboard',
    data() {
      return {
        projects: [],
        loading: false,
        color: '#41B883',
        size: '120px',
        margin: '2px',
        radius: '2px',
        widgetHeight: '',
        resizeTimer: ''
      }
    },
    computed: {
      ...mapGetters({
        authUser: 'authUser',
        update_projects: 'update_projects'
      })
    },
    watch: {
      update_projects: function(update) {
        if (update) {
          this.updateDashboard()
        }
        this.$store.dispatch('setUpdateProjects', false)
      }
    },
    methods: {
      updateDashboard() {
        this.loading = true;

        axios.get(GET_PROJECT_URL, userAuth.addAuthHeader() ).then( response => {
          this.projects = response.data.projects;
          this.loading = false
        });
      },
      setWidgetHeight() {
        this.widgetHeight = document.getElementById('create-widget').offsetHeight;
      },
      handleResize() {
        clearTimeout(this.resizeTimer);
        this.resizeTimer = setTimeout(() => {
          this.setWidgetHeight()
        }, 300);


      }
    },
    components: {
      Icon,
      ProjectWidget,
      RingLoader
    },
    mounted () {
      this.setWidgetHeight();
      this.updateDashboard();
      window.addEventListener('resize', this.handleResize)
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.handleResize)
    }
  };


</script>

<style scoped>

  .fa-icon {
    width: 45%;
    height: auto;
  }
  .loading {
    text-align:center;
    display: inline-block;
  }
  #create-widget {
    border: 1px solid #c6c6c6;
    border-radius: 20px;
    margin-bottom: 10px;
    padding-top: 10px;
  }
  .create {
    color: #41B883;
  }

</style>
