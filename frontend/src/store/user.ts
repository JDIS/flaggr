import { User } from '@/models/user'

const state = {
    connectedUser: null
}

const mutations = {
    setUser(storeState: any, user: User) {
      storeState.connectedUser = user;
    }
}

const actions = {
    connectUser(context: any, payload: any) {
      const user = new User(payload.username)
      context.commit('setUser', user) // TODO change to actually connect the user
    },

    disconnectUser(context: any) {
      context.commit('setUser', null) // TODO actually disconnect user
    }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
}
