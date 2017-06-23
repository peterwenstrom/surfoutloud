<template>
  <transition name="fade">
    <div class="widget"v-on:click="selectProject" v-bind:style="{height: widgetHeight + 'px'}">
      <a class="project-link" v-if="show">
        <div class="widget-top">
          <h6><strong>{{project.name}}</strong></h6>
          <p>{{project.description}}</p>
        </div>
        <div class="widget-bottom row">
          <div class="col-8">
            <p>Admin: {{project.admin}}</p>
          </div>
          <div class="col-4">
            <icon v-bind:name="project.icon" v-bind:style="{color: project.color}"></icon>
          </div>
        </div>
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
        // If widget is clicked pass project details to store and push to the specified project page
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
    border-radius: 5px;
    padding: 10px;
    cursor: pointer;
  }
  .widget-top {
    height: 70%;
    overflow: hidden;
  }
  .widget-top p {
    font-size: small;
  }
  .widget-bottom {
    height: 30%;
    min-height: 50px;
    width: 100%;
    overflow: hidden;
    background-color: #efefef;
    border-radius: 5px;
    text-align: left;
    vertical-align: middle;
    margin: 0;
    padding: 5px 0 5px 0;
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
    width: auto;
    height: 100%;
  }
</style>
