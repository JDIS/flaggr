import Vue from 'vue'
import Vuex from 'vuex'
import user from '@/store/user'
import network from '@/store/network'
import team from '@/store/team'

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user,
    network,
    team
  },
})
