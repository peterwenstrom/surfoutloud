import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import App from './App.vue'
import router from './router/index'
import axios from 'axios'
import socket from './socket/flask-socketio'
import store from './store/index'

Vue.use(BootstrapVue);

Vue.config.productionTip = false;

/* eslint-disable no-new (psst.. only to bypass lints rule, we can keep it for the time being) */
new Vue({
  el: '#app',
  router,
  axios,
  socket,
  store,
  template: '<App/>',
  components: { App }
});


