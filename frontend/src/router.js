import Vue from 'vue'
import Router from 'vue-router'
import BootstrapVue from 'bootstrap-vue';

import Hello from '@/components/Hello'
import Chat from '@/components/Chat'
import Bye from '@/components/Bye'
import ProjectView from '@/components/ProjectView'
import Login from '@/components/Login'
import Register from '@/components/Register'

Vue.use(BootstrapVue);

Vue.use(Router)

export default new Router({
/*  mode: 'history',*/ //Uncomment to remove the hashtag, transition is not smooth though...
  routes: [
    {
      path: '/hello',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/bye',
      name: 'Bye',
      component: Bye

    },
    {
      path: '/chat',
      name: 'Chat',
      component: Chat
    },
    {
      path: '/projectview',
      name: 'ProjectView',
      component: ProjectView
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    }

  ]
})
