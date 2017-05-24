import store from '../store'
import axios from 'axios'

const LOGIN_URL = API_URL + '/login';
const REGISTER_URL = API_URL + '/register';
const AUTH_URL = API_URL + '/auth';

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

  register (credentials, callback) {
    axios.post(REGISTER_URL, credentials).then(response => {
      localStorage.setItem('authUser', JSON.stringify(response.data));
      store.dispatch('setUserObject', response.data);
      callback(false);
    }).catch( error => {
      if(error.response) {
        callback(error.response.data.message);
      } else {
        callback('No response from the server, check your connection or try again later');
      }
    });
  },

  checkAuth () {
    return store.getters.authorized;
  },

  checkServerAuth (callback) {
    const user = JSON.parse(localStorage.getItem('authUser'));
    if(!user) {
      store.dispatch('clearUserObject');
      callback('login');
    } else {
      axios.post(AUTH_URL, user, {headers: {'Authorization': 'Bearer ' + user.access_token}}).then( () => {
        store.dispatch('setUserObject', user);
        callback('dashboard');
      }).catch( () => {
        store.dispatch('clearUserObject');
        localStorage.removeItem('authUser');
        callback('login');
      });
    }
  },

  refreshUser (user) {
    localStorage.setItem('authUser', user);
    store.dispatch('setUserObject', user);
  },

  addAuthHeader () {
    return {headers: {'Authorization': 'Bearer ' + store.getters.accessToken}}
  }

}
