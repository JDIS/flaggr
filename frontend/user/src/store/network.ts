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

    setError(storeState: any, error: boolean) {
      storeState.hasError = error;
    }
}

const actions = {
  addRequestInProgress(context: any) {
    context.commit('addRequest')
  },

  removeRequestInProgress(context: any) {
    context.commit('removeRequest')
  },

  setError(context: any, error: boolean) {
    context.commit('setError', error)
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations
}
