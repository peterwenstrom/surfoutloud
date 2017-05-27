<template>
  <div class="portfolio-item">
    <transition name="fade">
      <a class="project-link" v-if="show" v-on:click="selectProject">
        <p>{{project.name}}</p>
        <img class="img-portfolio img-responsive project" src="../assets/portfolio-2.jpg">
      </a>
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
    methods: {
      selectProject() {
        this.$store.dispatch('setProjectObject', this.project);
        this.$router.push('project')
      }
    },
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
  .project-link {
    color: #35495E;
  }
  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
    opacity: 0
  }
  a {
    cursor: pointer;
  }
</style>
