import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
<<<<<<< HEAD
import Chat from '@/components/Chat'
=======
import Bye from '@/components/Bye'
>>>>>>> 3f7615240c80913f74493145671431caf599cd9a

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
<<<<<<< HEAD
      path: '/chat',
      name: 'Chat',
      component: Chat
=======
      path: '/bye',
      name: 'Bye',
      component: Bye
>>>>>>> 3f7615240c80913f74493145671431caf599cd9a
    }
  ]
})
