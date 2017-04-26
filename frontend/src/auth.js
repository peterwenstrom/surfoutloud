import router from './router'
import axios from 'axios'

const API_URL = 'http://localhost:5000/'
const LOGIN_URL = API_URL + ''
const SIGNUP_URL = API_URL + ''

export default {

  user: {
    authenticated: false
  },

  login(creds, redirect) {
    axios.post(LOGIN_URL, creds, (data) => {
      localStorage.setItem('id_token', data.id_token)

      this.user.authenticated = true

      if(redirect) {
        router.go(redirect)
      }

    }).error((err) => {
      console.log("error in login post")
      console.log(err)
    })
  },

  signup(creds, redirect) {
    axios.post(SIGNUP_URL, creds, (data) => {
      localStorage.setItem('id_token', data.id_token)

      this.user.authenticated = true

      if(redirect) {
        router.go(redirect)
      }

    }).error((err) => {
      console.log("error in signup post")
      console.log(err)
    })
  },

  logout() {
    localStorage.removeItem('id_token')
    this.user.authenticated = false
  },

  checkAuth() {
    let jwt = localStorage.getItem('id_token')
    if(jwt) {
      this.user.authenticated = true
    } else {
      this.user.authenticated = false
    }
  },


  getAuthHeader() {
    return {
      'Authorization': 'Bearer ' + localStorage.getItem('id_token')
    }
  }
}
