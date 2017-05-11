import store from '../store'

const LOGIN_URL = '/api/login';
const REGISTER_URL = '/api/register';
const AUTH_URL = '/api/auth';

export default {
  login () {

  },

  logout () {
    store.dispatch('clearUserObject');
    localStorage.removeItem('authUser');
  },

  register () {

  },

  checkAuth () {

  },

  checkServerAuth () {

  },

  addAuthHeader () {

  }

}
