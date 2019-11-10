import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home.vue'
import store from '@/store'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/challenges',
      name: 'challenges',
      meta: { requiresAuth: true },
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/Challenges.vue'),
    },
    {
      path: '/scoreboard',
      name: 'scoreboard',
      component: () => import(/* webpackChunkName: "about" */ './views/Scoreboard.vue'),
    }
  ],
});

/**
 * If the client is connected, redirect it to where it pleases. If not, verify
 * if it is connected, then check routes permissions. This is called when accessing a page
 * (ex: /scoreboard) and upon page change (ex: client clicks on the challenges page)
 */
router.beforeEach((to, from, next) => {
  if (store.getters['user/isConnected']) {
    next()
  } else {
    store.dispatch('user/fetchUser').then((user) => {
      if (to.meta.requiresAuth) {
        console.log(store.getters['user/isConnected'])
        if (store.getters['user/isConnected']) {
          next()
        } else {
          next('/')
        }
      } else {
        next()
      }
    })
  }
})

export default router
