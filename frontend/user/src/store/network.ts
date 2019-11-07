/**
 * Store to manage network calls state (has an error happened during a call? Are there requests in progress? etc)
 */

const state = {
    requestsInProgress: [],
    hasError: false
}

const mutations = {
    addRequest(storeState: any) {
      storeState.requestsInProgress.push(true);
    },

    removeRequest(storeState: any) {
      storeState.requestsInProgress.pop();
    },

    setError(storeState: any) {
      storeState.hasError = true;
    }
}

const actions = {
  addRequestInProgress(context: any) {
    context.commit('addRequest')
  },

  removeRequestInProgress(context: any) {
    context.commit('removeRequest')
  },

  setError(context: any) {
    context.commit('setError')
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
}
