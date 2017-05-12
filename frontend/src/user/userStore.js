
const state = {
  user: {'access_token': '', 'username': ''},
  authorized: false
};

const getters = {
  authUser(state) {
    return state.user;
  },
  authorized(state) {
    return state.authorized;
  },
  accessToken(state) {
    return state.user.access_token;
  }
};

const mutations = {
  SET_AUTH_USER (state, userObject) {
    state.user = userObject;
    state.authorized = true
  },
  CLEAR_AUTH_USER (state) {
    state.user = {'access_token': '', 'username': ''};
    state.authorized = false
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
