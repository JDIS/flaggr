import Vue from 'vue';
import VueRouter, {Route} from 'vue-router';
import store from '@/store'
import {getEvents} from '@/services/event.service';
import {Event} from '@/models/event';

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  linkActiveClass: 'is-active',
  routes: [
    {
      path: '/',
      name: 'home',
      meta: {},
      component: () => import(/* webpackChunkName: "home" */ './views/Home.vue')
    },
    {
      path: '/:eventId',
      name: 'eventHome',
      meta: { requiresAuth: true },
      component: () => import(/* webpackChunkName: "home" */ './views/Home.vue')
    },
    {
      path: '/:eventId/event',
      name: 'event',
      meta: { requiresAuth: true },
      component: () => import(/* webpackChunkName: "event" */ './views/Event.vue')
    },
    {
      path: '/:eventId/challenges',
      name: 'challenges',
      meta: { requiresAuth: true },
      component: () => import(/* webpackChunkName: "challenges" */ './views/Challenges.vue')
    },
    {
      path: '/:eventId/challenges/edit/:id',
      name: 'edit-challenge',
      meta: { requiresAuth: true },
      props: true,
      component: () => import(/* webpackChunkName: "challenges" */ './views/Challenge.vue')
    },
    {
      path: '/:eventId/challenges/new',
      name: 'new-challenge',
      meta: { requiresAuth: true },
      props: true,
      component: () => import(/* webpackChunkName: "challenges" */ './views/Challenge.vue')
    },
    {
      path: '/:eventId/participants',
      name: 'participants',
      meta: { requiresAuth: true },
      component: () => import(/* webpackChunkName: "participants" */ './views/Participants.vue')
    }
  ],
});

/**
 * Fetch the list of events if it doesnt already exist. Set the current event according to the
 * route param.
 * @param to Route we're going to
 * @param from Route we're coming from
 */
function fetchEventsSetEventIfNeeded(to: Route, from: Route) {
  if (store.getters['event/events'].length === 0) {
    getEvents().then((events) => {
      store.dispatch('event/setEvents', events)
      const currentEvent = events.find((event) => event.id === parseInt(to.params.eventId, 0.4))
      store.dispatch('event/setEvent', currentEvent)
    })
  } else if (from.params.eventId !== to.params.eventId) {
    const currentEvent = store.getters['event/events'].find(
        (event: Event) => event.id === parseInt(to.params.eventId, 0.4))
    store.dispatch('event/setEvent', currentEvent)
  }

}

/**
 * If the client is connected, redirect it to where it pleases. If not, verify
 * if it is connected, then check routes permissions. This is called when accessing a page
 * and upon page change (ex: client clicks on the challenges page)
 */
router.beforeEach((to, from, next) => {
  fetchEventsSetEventIfNeeded(to, from);
  if (store.getters['admin/isConnected']) {
    next()
  } else {
    if (to.meta.requiresAuth) {
      store.dispatch('admin/fetchAdmin').then((partcipant) => {
        if (to.meta.requiresAuth) {
          if (store.getters['admin/isConnected']) {
            next()
          } else {
            next(`/`)
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


export default router;
