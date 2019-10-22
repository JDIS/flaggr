import { User } from '@/models/user'
import axios from 'axios'

/**
 * Store to manage the connected user's information.
 */

const state = {
    connectedUser: null
}

const mutations = {
    setUser(storeState: any, user: User) {
      storeState.connectedUser = user;
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
      .then((response) => {
        console.log('connection success', response)
        context.commit('setUser', response.data as User)
      })
      .catch((error) => {
        console.log('error during login:', error)
        // TODO handle errors
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
      .then((response) => {
        console.log('user registred', response)
        context.commit('setUser', response.data as User)
        // context.commit('setUser', user)
      })
      .catch((error) => {
        console.log('error during register:', error.response)
        // TODO handle errors
      })
  },

  disconnectUser(context: any) {
    axios.post('logout')
      .then((response) => {
        context.commit('setUser', null)
      })
      .catch((error) => {
        console.log('error during logout:', error)
      })
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
}
