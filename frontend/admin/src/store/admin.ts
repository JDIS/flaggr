import axios, {AxiosError, AxiosResponse} from 'axios'
import {sendAlertWithVariables, sendErrorAlert} from '@/helpers/alerts.helper'
import store from '../store'
import route from '../router'
import {Admin} from '@/models/admin';

/**
 * Store to manage the connected admin's information.
 */

const state = {
  connectedAdmin: null,
  /**
   * Development only
   */
  creds: null
}

const mutations = {
  setAdmin(storeState: any, admin: Admin) {
    storeState.connectedAdmin = admin;
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
    return storeState.connectedAdmin !== null
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
    route.push(`/login`)
  }
}

const actions = {
  /**
   * Send a request to connect the admin. Upon successful connection,
   * set the admin's information in the app's state.
   * @param context VueX context
   * @param payload Data to connect the user (email, pass)
   */
  connectAdmin(context: any, payload: any) {
    payload.remember = true // To change later
    axios.post('admin/login', payload)
      .then((response: AxiosResponse) => {
        context.commit('setAdmin', response.data as Admin)
        context.commit('setCreds', btoa(`${payload.email}:${payload.password}`))
        store.dispatch('admin/fetchAdmin')
        route.push('/')
      }).catch((error) => {
        sendAlertWithVariables('login.error', {error: error.response.data.message})
    })
  },

  disconnectAdmin(context: any) {
    axios.get('logout')
      .then((response: AxiosResponse) => {
        context.commit('setAdmin', null)
        context.commit('setCreds', null)
        checkPermissions()
      })
      .catch((error: AxiosError) => {
        sendErrorAlert('logout.error', error)
      })
  },

  /**
   * Fetches the current admin to set in the store.
   * If not connected, sets the state accordingly.
   * If the admin is in a route that requires authentication,
   * redirect to login page.
   * @param context VueX Store context.
   */
  fetchAdmin(context: any) {
    return axios.get(`admin/admin`)
      .then((response: AxiosResponse<Admin>) => {
        context.commit('setAdmin', response.data)
      })
      .catch((error: AxiosError) => {
        context.commit('setAdmin', null)
        context.commit('setCreds', null)
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
