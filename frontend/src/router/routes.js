import Dashboard from '../components/dashboard/Dashboard.vue'
import Login from '../components/login/Login.vue'
import Register from '../components/register/Register.vue'
import Profile from '../components/profile/Profile.vue'
import Project from '../components/project/Project.vue'
import CreateProject from '../components/create_project/CreateProject.vue'


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
    path: '/createproject',
    name: 'CreateProject',
    component: CreateProject,
    meta: {requiresAuth: true}
  }
];

export default routes;
