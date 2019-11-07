import Vue from 'vue'
import Vuex from 'vuex'
import network from './network'

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    network
  }
})
