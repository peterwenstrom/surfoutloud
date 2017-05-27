import Vue from 'vue'
import Vuex from 'vuex'

import userStore from './user/userStore'
import projectStore from './project/projectStore'

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {userStore, projectStore}
})
