<template>
  <div class="portfolio-item">
    <transition name="fade">
      <!--<router-link v-if="show" :to="{ path: '/project', query: { attr:'project' }}">-->
        <router-link v-if="show" :to="{  path: '/project', query: { attr: project[0]}}">
        <p>Project {{project[0]}}</p>
        <img class="img-portfolio img-responsive project" src="../assets/portfolio-2.jpg">
      </router-link>
    </transition>

  </div>
</template>

<script>
  export default {
    data () {
      return {
        show: false
      }
    },
    props: ['project'],
    mounted() {
        this.show = true;
    }
  }
</script>

<style scoped>
  .portfolio-item {
    margin-bottom: 10px;
  }
  .project {
    width: 80%;
    height: 80%;
  }
  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
    opacity: 0
  }
</style>
