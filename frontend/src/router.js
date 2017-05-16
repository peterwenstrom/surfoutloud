import Vue from 'vue'
import Router from 'vue-router'

import Chat from '@/components/Chat'
import Dashboard from '@/components/Dashboard'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Project from '@/components/Project'
import CreateNewProject from '@/components/CreateNewProject'

import user from './user/userAuth'

Vue.use(Router);

const router = new Router({
/*  mode: 'history',*/ //Uncomment to remove the hashtag, transition is not smooth though...
  routes: [
    {
      path: '/chat',
      name: 'Chat',
      component: Chat,
      meta: {requiresAuth: true}
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard,
      meta: {requiresAuth: true}
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
      component: Project,
      meta: {requiresAuth: true}
    },
    {
      path: '/createnewproject',
      name: 'CreateNewProject',
      component: CreateNewProject,
      meta: {requiresAuth: true}
    }

  ]
});

router.beforeEach((to, from, next) => {
  if(to.meta.requiresAuth) {
    if(user.checkAuth()) {
      next();
    }
    else {
      next('/login');
    }
  } else {
    next()
  }
});

export default router;
