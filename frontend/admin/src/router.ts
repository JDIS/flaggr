import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from './views/Home.vue';

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  linkActiveClass: 'is-active',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/event',
      name: 'event',
      component: () => import(/* webpackChunkName: "event" */ './views/Event.vue')
    },
    {
      path: '/challenges',
      name: 'challenges',
      component: () => import(/* webpackChunkName: "challenges" */ './views/Challenges.vue')
    },
    {
      path: '/challenges/edit/:id',
      name: 'edit-challenge',
      props: true,
      component: () => import(/* webpackChunkName: "challenges" */ './views/Challenge.vue')
    },
    {
      path: '/challenges/new',
      name: 'new-challenge',
      props: true,
      component: () => import(/* webpackChunkName: "challenges" */ './views/Challenge.vue')
    },
    {
      path: '/participants',
      name: 'participants',
      component: () => import(/* webpackChunkName: "participants" */ './views/Participants.vue')
    }
  ],
});

export default router;
