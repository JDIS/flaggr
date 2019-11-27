import Vue from 'vue'
import Vuex from 'vuex'
import participant from '@/store/participant'
import network from '@/store/network'
import team from '@/store/team'
import event from '@/store/event'

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    participant,
    network,
    team,
    event
  },
})
