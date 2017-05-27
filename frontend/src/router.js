import Vue from 'vue'
import Router from 'vue-router'

import Dashboard from '@/components/Dashboard'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Profile from '@/components/Profile'
import Project from '@/components/Project'
import CreateNewProject from '@/components/CreateNewProject'

import user from './user/userAuth'

Vue.use(Router);

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'None',
      redirect: { name: 'Login' }
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
      component: Login,
      meta: {requiresAuth: false}
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      meta: {requiresAuth: false}
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile,
      meta: {requiresAuth: true}
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
  const second_time = localStorage.getItem('second_time');
  if (from.fullPath === '/' && !second_time) {
    localStorage.setItem('second_time', true);
    user.checkServerAuth( redirect => {
      if (redirect === '/') {
        next('dashboard')
      } else {
        next(redirect)
      }
    })
  } else {
    localStorage.removeItem('second_time');
    if (to.meta.requiresAuth) {
      if (user.checkAuth()) {
        next();
      }
      else {
        next('/login');
      }
    } else if (!to.meta.requiresAuth) {
      if (!user.checkAuth()) {
        next();
      }
      else {
        next('/dashboard');
      }
    } else {
      next()
    }
  }
});

router.afterEach((to, from) => {


});

export default router;
