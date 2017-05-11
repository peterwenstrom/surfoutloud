<template>
  <div class="portfolio-item">
    <router-link to="/project">
      <p>Project {{project[0]}}</p>
      <img class="img-portfolio img-responsive project" src="../assets/portfolio-2.jpg">
    </router-link>
  </div>
</template>

<script>
  export default {
    props: ['project']
  }
</script>

<style scoped>

</style>
