
const state = {
  authUser: {'access_token': '', 'username': ''}
};

const getters = {
  authUser(state) {
    return state.authUser;
  }
};

const mutations = {
  SET_AUTH_USER (state, userObject) {
    state.authUser = userObject
  },
  CLEAR_AUTH_USER (state) {
    state.authUser = {'access_token': '', 'username': ''}
  }
};

const actions = {
  setUserObject: ({commit}, userObject) => {
    commit('SET_AUTH_USER', userObject)
  },
  clearUserObject: ({commit}) => {
    commit('CLEAR_AUTH_USER')
  }
};

export default {
  state,
  getters,
  mutations,
  actions
}
