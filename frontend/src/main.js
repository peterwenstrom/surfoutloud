import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import App from './App'
import router from './router'
import axios from 'axios'

import store from './store/index'

Vue.use(BootstrapVue);

Vue.config.productionTip = false;

/* eslint-disable no-new (psst.. only to bypass lints rule, we can keep it for the time being) */
new Vue({
  el: '#app',
  router,
  axios,
  store,
  template: '<App/>',
  components: { App }
});


