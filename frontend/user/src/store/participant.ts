import axios, { AxiosError, AxiosResponse } from 'axios'
import { sendAlert, sendAlertWithVariables } from '@/helpers'
import store from '../store'
import route from '../router'
import { Participant } from '@/models/participant'

/**
 * Store to manage the connected participant's information.
 */

const state = {
  connectedParticipant: null,
  /**
   * Development only
   */
  creds: null
}

const mutations = {
  setParticipant(storeState: any, participant: Participant) {
    storeState.connectedParticipant = participant;
  },
  setCreds(storeState: any, creds: string) {
    if (process.env.VUE_APP_DEBUG === '1') {
      storeState.creds = creds;
      localStorage.setItem('creds', creds)
    }
  }
}

const getters = {
  isConnected: (storeState: any) => {
    return storeState.connectedParticipant !== null
  },
  creds: (storeState: any) => {
    if (process.env.VUE_APP_DEBUG === '1') {
      if (storeState.creds) {
        return storeState.creds
      } else {
        return localStorage.getItem('creds')
      }
    }
  }
}

/**
 * Check to see if the current route requires auth.
 * This function should only be called if we know the client
 * is not connected.
 */
function checkPermissions() {
  if (route.currentRoute.meta.requiresAuth === true) {
    route.replace(`/${route.currentRoute.params.eventId}`)
  }
}

const actions = {
  /**
   * Send a request to connect the participant. Upon successful connection,
   * set the participant's information in the app's state.
   * @param context VueX context
   * @param payload Data to connect the user (email, pass)
   */
  connectParticipant(context: any, payload: any) {
    payload.remember = true // To change later
    axios.post('login', payload, {data: {withEvent: true}})
      .then((response: AxiosResponse) => {
        context.commit('setParticipant', response.data as Participant)
        context.commit('setCreds', btoa(`${payload.email}:${payload.password}`))
        store.dispatch('participant/fetchParticipant')
      })
      .catch((error: AxiosError) => {
        if (error.response!.status === 422) {
          sendAlert('signin.invalidCreds')
        } else {
          console.log('error during login:', error)
        }
      })
  },

  /**
   * Send a request to register a new user. Upon successful registration,
   * set the user's information in the app's state.
   * @param context VueX context
   * @param payload Data to register the user (email, pass, username)
   */
  registerParticipant(context: any, payload: any) {
    axios.post('register', payload, {data: {withEvent: true}})
      .then((response: AxiosResponse) => {
        store.dispatch('participant/fetchParticipant')
        context.commit('setCreds', btoa(`${payload.email}:${payload.password}`))
        // context.commit('setUser', user)
      })
      .catch((error: AxiosError) => {
        if (error.response!.status === 422) {
          sendAlertWithVariables('signup.error', {error: error.response!.data.message})
        } else {
          console.log('error during register:', error.response)
        }
      })
  },

  disconnectParticipant(context: any) {
    axios.get('logout')
      .then((response: AxiosResponse) => {
        context.commit('setParticipant', null)
        context.commit('setCreds', null)
        checkPermissions()
        store.dispatch('team/fetchTeam')
      })
      .catch((error: AxiosError) => {
        console.log('error during logout:', error)
      })
  },

  /**
   * Fetches the current participant to set in the store.
   * If not connected, sets the state accordingly.
   * If the participant is in a route that requires authentication,
   * redirect to home page.
   * @param context VueX Store context.
   */
  fetchParticipant(context: any, eventId: number) {
    return axios.get(`/participant`)
      .then((response: AxiosResponse<Participant>) => {
        context.commit('setParticipant', response.data)
        store.dispatch('team/fetchTeam')
      })
      .catch((error: AxiosError) => {
        context.commit('setParticipant', null)
        checkPermissions()
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
