import router from './router'
import axios from 'axios'

const API_URL = 'http://localhost:5000/'
const LOGIN_URL = API_URL + 'login'
const REGISTER_URL = API_URL + 'register'

export default {

  user: {
    authenticated: false
  },

  login(credentials, redirect) {
    axios.post(LOGIN_URL, credentials).then( response => {
      localStorage.setItem('id_token', response.data.access_token)

      this.user.authenticated = true

/*      if(redirect) {
        router.go(redirect)
      }*/

    }).catch( err => {
      console.log("error in login post")
      console.log(err)
    })
  },

  register(credentials, redirect) {
    axios.post(REGISTER_URL, credentials).then( response => {
      localStorage.setItem('id_token', response.data.access_token)

      this.user.authenticated = true

/*      if(redirect) {
        router.go(redirect)
      }*/

    }).catch( err => {
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
    return 'JTW ' + localStorage.getItem('id_token')
  }
}
