<template>

  <div class="row">
    <div class="col-lg-10 col-lg-offset-1 text-center">
      <h2>Project overview</h2>
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
            <p>Project 1</p>
            <a href="#">
              <img class="img-portfolio img-responsive" src="static/img/portfolio-2.jpg">
            </a>
          </div>
        </div>
        <div class="col-md-3">
          <div class="portfolio-item">
            <p>Project 2</p>
            <a href="#">
              <img class="img-portfolio img-responsive" src="static/img/portfolio-3.jpg">
            </a>
          </div>
        </div>
        <div class="col-md-3">
          <div class="portfolio-item">
            <p>Project 3</p>
            <a href="#">
              <img class="img-portfolio img-responsive" src="static/img/portfolio-4.jpg">
            </a>
          </div>
        </div>
        <div class="col-md-3">
          <div class="portfolio-item">
            <p>Project 4</p>
            <a href="#">
              <img class="img-portfolio img-responsive" src="static/img/portfolio-4.jpg">
            </a>
          </div>
        </div>
        <div class="col-md-3">
          <div class="portfolio-item">
            <p>Project 5</p>
            <a href="#">
              <img class="img-portfolio img-responsive" src="static/img/portfolio-4.jpg">
            </a>
          </div>
        </div>
        <div class="col-md-3">
          <div class="portfolio-item">
            <p>Project 6</p>
            <a href="#">
              <img class="img-portfolio img-responsive" src="static/img/portfolio-4.jpg">
            </a>
          </div>
        </div>
        <div class="col-md-3">
          <div class="portfolio-item">
            <p>Project 7</p>
            <a href="#">
              <img class="img-portfolio img-responsive" src="static/img/portfolio-4.jpg">
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
        msg: ""
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
  .glyphicon.glyphicon-plus {
    font-size: 100px;
  }

</style>
