
const state = {
  project: {
    name: '',
    id: '',
    admin: '',
    description: ''
  }
};

const getters = {
  project(state) {
    return state.project;
  }
};

const mutations = {
  SET_PROJECT (state, projectObject) {
    state.project = projectObject
  },
  CLEAR_PROJECT (state) {
    state.project = {
      name: '',
      id: '',
      admin: '',
      description: ''
    }
  }
};

const actions = {
  setProjectObject: ({commit}, userObject) => {
    commit('SET_PROJECT', userObject)
  },
  clearProjectObject: ({commit}) => {
    commit('CLEAR_PROJECT')
  }
};

export default {
  state,
  getters,
  mutations,
  actions
}
