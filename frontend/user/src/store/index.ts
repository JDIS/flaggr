import Vue from 'vue'
import Vuex from 'vuex'
import participant from '@/store/participant'
import network from '@/store/network'
import team from '@/store/team'

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    participant,
    network,
    team
  },
})
