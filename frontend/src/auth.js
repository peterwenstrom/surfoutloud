import router from './router'
import axios from 'axios'

const API_URL = 'http://localhost:5000/';
const LOGIN_URL = API_URL + 'login';
const REGISTER_URL = API_URL + 'register';

export default {

  user: {
    authenticated: false
  },

  login(credentials, redirect, callback) {
    axios.post(LOGIN_URL, credentials).then( response => {
      localStorage.setItem('id_token', response.data.access_token);

      this.user.authenticated = true;

      router.push(redirect);
      callback(true);

    }).catch( err => {
      console.log("error in login post");
      console.log(err);
      callback(false);
    })
  },

  register(credentials, redirect, callback) {
    axios.post(REGISTER_URL, credentials).then( response => {
      localStorage.setItem('id_token', response.data.access_token);

      this.user.authenticated = true;

      router.push(redirect);
      callback(true);
    }).catch( err => {
      callback(false, err.response.data.msg);
    })
  },

  logout(redirect) {
    localStorage.removeItem('id_token');
    this.user.authenticated = false;
    router.push(redirect);
  },

  checkAuth() {
    let jwt = localStorage.getItem('id_token');
    if(jwt) {
      this.user.authenticated = true;
    } else {
      this.user.authenticated = false;
    }
  },

  getAuthHeader() {
    return {headers: {'Authorization': 'Bearer ' + localStorage.getItem('id_token')}}
  }
}