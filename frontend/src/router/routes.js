import Dashboard from '@/components/Dashboard'
import Login from '@/components/Login'
import Register from '@/components/Register'
import Profile from '@/components/Profile'
import Project from '@/components/Project'
import CreateNewProject from '@/components/CreateNewProject'


const routes = [
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
    path: '/project/:project_id',
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
];

export default routes;
