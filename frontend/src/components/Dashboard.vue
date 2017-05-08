<template>

  <div class="row">
    <div class="col-lg-12 text-center">
      <h2>Dashboard</h2>
      <hr class="small">
      <div class="row">
        <div class="col-md-3">
          <div class="portfolio-item">
            <p>Create new project</p>
            <a href="#">
              <span class="glyphicon glyphicon-plus"></span>
            </a>
          </div>
        </div>
        <div class="col-md-3">
          <div class="portfolio-item">
            <router-link to="/project">
              <p>Project 1</p>
              <img class="img-portfolio img-responsive project" src="static/img/portfolio-2.jpg">
            </router-link>
          </div>
        </div>
        <div class="col-md-3">
          <div class="portfolio-item">
            <p>Project 2</p>
            <a>
              <img class="img-portfolio img-responsive project" src="static/img/portfolio-3.jpg">
            </a>
          </div>
        </div>
        <div class="col-md-3">
          <div class="portfolio-item">
            <p>Project 3</p>
            <a>
              <img class="img-portfolio img-responsive project" src="static/img/portfolio-4.jpg">
            </a>
          </div>
        </div>
        <div class="col-md-3">
          <div class="portfolio-item">
            <p>Project 4</p>
            <a>
              <img class="img-portfolio img-responsive project" src="static/img/portfolio-4.jpg">
            </a>
          </div>
        </div>
        <div class="col-md-3">
          <div class="portfolio-item">
            <p>Project 5</p>
            <a>
              <img class="img-portfolio img-responsive project" src="static/img/portfolio-4.jpg">
            </a>
          </div>
        </div>
        <div class="col-md-3">
          <div class="portfolio-item">
            <p>Project 6</p>
            <a>
              <img class="img-portfolio img-responsive project" src="static/img/portfolio-4.jpg">
            </a>
          </div>
        </div>
        <div class="col-md-3">
          <div class="portfolio-item">
            <p>Project 7</p>
            <a>
              <img class="img-portfolio img-responsive project" src="static/img/portfolio-4.jpg">
            </a>
          </div>
        </div>
      </div>
      <!-- /.row (nested) -->
    </div>
    <!-- /.col-lg-10 -->

  </div>



</template>

<script>

  export default {
    name: 'Dashboard',
    data() {
      return {

      }
    },
    methods: {
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

</style>
