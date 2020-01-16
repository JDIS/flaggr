import axios, { AxiosError, AxiosResponse } from 'axios'
import { Team } from '@/models/team'
import { Event } from '@/models/event'
import route from '@/router';


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

/**
 * If the current route requires an open event, redirect to home.
 * This function should only be called if we know the event is not opened.
 */
function checkPermissions() {
  if (route.currentRoute.meta.requiresOpenEvent === true) {
    route.push(`/${route.currentRoute.params.eventId}`)
  }
}

const actions = {
  /**
   * Fetch the event from the server and set the state accordingly.
   * @param context vuex context
   */
  fetchEvent(context: any, eventId: number) {
    axios.get(`event/${eventId}`)
      .then((response: AxiosResponse<Event>) => {
        context.commit('setEvent', response.data)
        if (!response.data.is_open) {
          checkPermissions()
        }
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
