// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false

/* eslint-disable no-new (psst.. only to bypass lints rule, we can keep it for the time being) */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})


