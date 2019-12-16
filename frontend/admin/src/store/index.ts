import Vue from 'vue'
import Vuex from 'vuex'
import network from './network'
import admin from '@/store/admin';
import event from '@/store/event';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    network,
    admin,
    event
  }
})
