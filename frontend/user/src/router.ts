import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'eventSelection',
      component: () => import(/* webpackChunkName: "eventSelection" */ './views/EventSelection.vue'),
      meta: { title: 'title.eventSelection'},
    },
    {
      path: '/:eventId',
      name: 'home',
      component: () => import(/* webpackChunkName: "home" */ './views/Home.vue'),
      meta: { title: 'title.home' , showNavbar: true},
    },
    {
      path: '/:eventId/challenges',
      name: 'challenges',
      meta: { title: 'title.challenges', showNavbar: true,
        requiresAuth: true, requiresTeam: true},
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "challenges" */ './views/Challenges.vue'),
    },
    {
      path: '/:eventId/scoreboard',
      name: 'scoreboard',
      meta: { title: 'title.scoreboard', showNavbar: true},
      component: () => import(/* webpackChunkName: "scoreboard" */ './views/Scoreboard.vue'),
    }
  ],
});

/**
 * If the client is connected, redirect it to where it pleases. If not, verify
 * if it is connected, then check routes permissions. This is called when accessing a page
 * (ex: /scoreboard) and upon page change (ex: client clicks on the challenges page)
 */
router.beforeEach((to, from, next) => {
  if (store.getters['participant/isConnected']) {
    next()
  } else {
    // This weird comparison is due to the fact that '0' == false in JS 😡
    if (parseInt(to.params.eventId, 0.4) >= 0) {
      store.dispatch('event/fetchEvent', to.params.eventId)
      store.dispatch('participant/fetchParticipant').then((partcipant) => {
        if (to.meta.requiresAuth) {
          if (store.getters['participant/isConnected']) {
            next()
          } else {
            next(`/${to.params.eventId}`)
          }
        } else {
          next()
        }
      })
    } else {
      next()
    }
  }
})

export default router
