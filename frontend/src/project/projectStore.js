
const state = {
  project: {
    name: '',
    id: '',
    admin: '',
    description: '',
    icon: '',
    color: ''
  },
  project_selected: false,
  update_projects: false
};

const getters = {
  project(state) {
    return state.project;
  },
  project_selected(state) {
    return state.project_selected
  },
  update_projects(state) {
    return state.update_projects
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
      description: '',
      icon: '',
      color: ''
    };
    state.project_selected = false
  },
  SET_UPDATE_PROJECTS (state, update) {
    state.update_projects = update
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
