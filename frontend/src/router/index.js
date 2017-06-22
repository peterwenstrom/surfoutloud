import Vue from 'vue'
import Router from 'vue-router'

import routes from './routes'

import userService from '../store/user/userService'
import store from '../store/index'

Vue.use(Router);

const router = new Router({
  routes: routes
});

router.beforeEach((to, from, next) => {
  const second_time = localStorage.getItem('second_time');
  if (from.fullPath === '/' && !second_time) {
    localStorage.setItem('second_time', true);
    userService.checkServerAuth( redirect => {
      if (redirect === '/') {
        next('dashboard')
      } else {
        next(redirect)
      }
    })
  } else {
    localStorage.removeItem('second_time');
    if (to.meta.requiresAuth) {
      if (store.getters.authorized) {
        next();
      }
      else {
        next('/login');
      }
    } else if (!to.meta.requiresAuth) {
      if (!store.getters.authorized) {
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

export default router;
