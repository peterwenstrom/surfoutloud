<template>

  <div class="row">
    <div class="col-lg-12 text-center">
      <h2>Dashboard</h2>
      <hr class="small">
      <div class="row">
        <div class="col-md-3 col-sm-6">
          <div class="portfolio-item">
            <p>Create new project</p>
            <icon name="plus-circle"></icon>
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
      </div>
    </div>

  </div>



</template>

<script>
  import 'vue-awesome/icons/plus-circle'
  import Icon from 'vue-awesome/components/Icon'

  export default {
    name: 'Dashboard',
    data() {
      return {

      }
    },
    methods: {
    },
    components: {
        Icon
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
