import { User } from '@/models/user'
import axios, { AxiosError, AxiosResponse } from 'axios'
import { sendAlert, sendAlertWithVariables } from '@/helpers'
import store from '../store'
import route from '../router'

/**
 * Store to manage the connected user's information.
 */

const state = {
  connectedUser: null,
  /**
   * Development only
   */
  creds: null
}

const mutations = {
  setUser(storeState: any, user: User) {
    storeState.connectedUser = user;
  },
  setCreds(storeState: any, creds: string) {
    if (process.env.VUE_APP_DEBUG) {
      storeState.creds = creds;
      localStorage.setItem('creds', creds)
    }
  }
}

const getters = {
  isConnected: (storeState: any) => {
    return storeState.connectedUser !== null
  },
  creds: (storeState: any) => {
    if (process.env.VUE_APP_DEBUG) {
      if (storeState.creds) {
        return storeState.creds
      } else {
        return localStorage.getItem('creds')
      }
    }
  }
}

function checkPermissions() {
  if (route.currentRoute.meta.requiresAuth === true) {
    route.replace('/')
  }
}

const actions = {
  /**
   * Send a request to connect the user. Upon successful connection,
   * set the user's information in the app's state.
   * @param context VueX context
   * @param payload Data to connect the user (email, pass)
   */
  connectUser(context: any, payload: any) {
    payload.remember = true // To change later
    axios.post('login', payload)
      .then((response: AxiosResponse) => {
        context.commit('setCreds', btoa(`${payload.email}:${payload.password}`))
        store.dispatch('user/fetchUser')
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
  registerUser(context: any, payload: any) {
    axios.post('register', payload)
      .then((response: AxiosResponse) => {
        store.dispatch('user/fetchUser')
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

  disconnectUser(context: any) {
    axios.get('logout')
      .then((response: AxiosResponse) => {
        context.commit('setUser', null)
        context.commit('setCreds', null)
        checkPermissions()
      })
      .catch((error: AxiosError) => {
        console.log('error during logout:', error)
      })
  },

  /**
   * Fetches the current user to set in the store.
   * If not connected, sets the state accordingly.
   * If the user is in a route that requires authentication,
   * redirect to home page.
   * @param context VueX Store context.
   */
  fetchUser(context: any) {
    return axios.get('user')
      .then((response: AxiosResponse<User>) => {
        context.commit('setUser', response.data)
        store.dispatch('team/fetchTeam')
      })
      .catch((error: AxiosError) => {
        context.commit('setUser', null)
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
