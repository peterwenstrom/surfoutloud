
const state = {
  project: {
    name: '',
    id: '',
    admin: '',
    description: '',
    icon: '',
    color: ''
  },
  projectSelected: false,
  updateProjects: false
};

const getters = {
  project(state) {
    return state.project;
  },
  projectSelected(state) {
    return state.projectSelected
  },
  updateProjects(state) {
    return state.updateProjects
  }
};

const mutations = {
  SET_PROJECT (state, projectObject) {
    state.project = projectObject;
    state.projectSelected = true
  },
  CLEAR_PROJECT (state) {
    state.project = {
      name: '',
      id: '',
      admin: '',
      description: '',
      icon: '',
      color: ''
    };
    state.projectSelected = false
  },
  SET_UPDATE_PROJECTS (state, update) {
    state.updateProjects = update
  }
};

const actions = {
  setProjectObject: ({commit}, userObject) => {
    commit('SET_PROJECT', userObject)
  },
  clearProjectObject: ({commit}) => {
    commit('CLEAR_PROJECT')
  },
  setUpdateProjects: ({commit}, update) => {
    commit('SET_UPDATE_PROJECTS', update)
  }
};

export default {
  state,
  getters,
  mutations,
  actions
}
