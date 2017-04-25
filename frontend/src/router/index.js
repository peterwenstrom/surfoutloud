import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Chat from '@/components/Chat'
import Bye from '@/components/Bye'


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
    }

  ]
})
