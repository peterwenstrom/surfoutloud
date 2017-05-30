<template>
  <transition name="fade">
    <div class="widget"v-on:click="selectProject" v-bind:style="{height: widgetHeight + 'px'}">

      <a class="project-link" v-if="show">
        <p><strong>{{project.name}}</strong></p>
        <p>Admin: {{project.admin}}</p>
        <icon name="diamond"></icon>
      </a>


    </div>
  </transition>
</template>

<script>
  import Icon from 'vue-awesome/components/Icon'
  import 'vue-awesome/icons/plus-circle'
  import 'vue-awesome/icons/window-close-o'
  import 'vue-awesome/icons/superpowers'
  import 'vue-awesome/icons/snowflake-o'
  import 'vue-awesome/icons/anchor'
  import 'vue-awesome/icons/heart'
  import 'vue-awesome/icons/diamond'
  import 'vue-awesome/icons/hand-spock-o'
  import 'vue-awesome/icons/globe'
  import 'vue-awesome/icons/star'
  import 'vue-awesome/icons/paw'
  import 'vue-awesome/icons/glass'

  export default {
    data () {
      return {
        show: false,
        size: '100px'
      }
    },
    props: ['project', 'widgetHeight'],
    methods: {
      selectProject() {
        this.$store.dispatch('setProjectObject', this.project);
        this.$router.push('project/' + this.project.id)
      }
    },
    mounted() {
      this.show = true
    },
    components: {
      Icon
    }
  }
</script>

<style scoped>
  .widget {
    margin-bottom: 10px;
    border: 1px solid #c6c6c6;
    border-radius: 20px;
    padding: 10px;
    cursor: pointer;
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
  .fa-icon {
    width: 20%;
    height: auto;
  }
</style>
