import {Event} from '@/models/event'


/**
 * Store to manage the current event.
 */

const state = {
  event: null,
  events: [] as Event[]
}

const mutations = {
  setEvent(storeState: any, event: Event) {
    storeState.event = event;
  },

  setEvents(storeState: any, events: Event[]) {
    storeState.events = events;
  }
}

const getters = {
  hasEvent: (storeState: any) => {
    return storeState.event !== null
  },

  events: (storeState: any) => {
    return storeState.events
  }
}

const actions = {
  /**
   * Set the current event.
   * @param context vuex context
   * @param event
   */
  setEvent(context: any, event: Event) {
    context.commit('setEvent', event)
  },

  /**
   * Set the list of available events.
   * @param context vuex context
   * @param events
   */
  setEvents(context: any, events: Event[]) {
    context.commit('setEvents', events)
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
}
