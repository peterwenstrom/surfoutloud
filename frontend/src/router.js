import Vue from 'vue'
import Router from 'vue-router'

import Hello from '@/components/Hello'
import Chat from '@/components/Chat'
import Dashboard from '@/components/Dashboard'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Project from '@/components/Project'

Vue.use(Router);

export default new Router({
/*  mode: 'history',*/ //Uncomment to remove the hashtag, transition is not smooth though...
  routes: [
    {
      path: '/hello',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/chat',
      name: 'Chat',
      component: Chat
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard
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
    },
    {
      path: '/project',
      name: 'Project',
      component: Project
    }

  ]
})
