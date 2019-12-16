import axios, { AxiosError, AxiosResponse } from 'axios'
import { Team } from '@/models/team'
import { Event } from '@/models/event'


/**
 * Store to manage the current event.
 */

const state = {
  event: null,
}

const mutations = {
  setEvent(storeState: any, event: Event) {
    storeState.event = event;
  }
}

const getters = {
  hasEvent: (storeState: any) => {
    return storeState.event !== null
  }
}

const actions = {
  /**
   * Fetch the event from the server and set the state accordingly.
   * @param context vuex context
   */
  fetchEvent(context: any, eventId: number) {
    axios.get(`event/${eventId}`)
      .then((response: AxiosResponse<Team>) => {
        context.commit('setEvent', response.data)
      })
      .catch((error: AxiosError) => {
        context.commit('setEvent', null)
      })
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
}
