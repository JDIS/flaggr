import Vue from 'vue'
import Vuex from 'vuex'
import user from '@/store/user'
import network from '@/store/network'

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user,
    network
  },
})
