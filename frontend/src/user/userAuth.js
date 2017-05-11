import store from '../store'
import axios from 'axios'

const LOGIN_URL = '/api/login';
const REGISTER_URL = '/api/register';
const AUTH_URL = '/api/auth';

export default {
  login (credentials, callback) {
    axios.post(LOGIN_URL, credentials).then(response => {
      localStorage.setItem('authUser', JSON.stringify(response.data));
      store.dispatch('setUserObject', response.data);
      callback(false);
    }).catch( error => {
      if (error.response) {
        callback(error.response.data.message);
      } else {
        callback('No response from the server, check your connection or try again later')
      }
    });
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
