
const state = {
  project: {
    name: '',
    id: '',
    admin: '',
    description: ''
  },
  project_selected: false
};

const getters = {
  project(state) {
    return state.project;
  },
  project_selected(state) {
    return state.project_selected
  }
};

const mutations = {
  SET_PROJECT (state, projectObject) {
    state.project = projectObject;
    state.project_selected = true
  },
  CLEAR_PROJECT (state) {
    state.project = {
      name: '',
      id: '',
      admin: '',
      description: ''
    };
    state.project_selected = false
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
