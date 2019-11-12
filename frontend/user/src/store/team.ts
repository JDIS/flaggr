import axios, { AxiosError, AxiosResponse } from 'axios'
import { Team } from '@/models/team'

/**
 * Store to manage the connected user's team.
 */

const state = {
  userTeam: null,
}

const mutations = {
  setTeam(storeState: any, team: Team) {
    storeState.userTeam = team;
  },
}

const getters = {
  hasTeam: (storeState: any) => {
    console.log('hasteam', storeState.userTeam)
    return storeState.userTeam !== null && JSON.stringify(storeState.userTeam) !== '{}'
  },
}

const actions = {
  /**
   * Fetch the team from the server and set the state accordingly.
   * @param context vuex context
   */
  fetchTeam(context: any) {
    axios.get('team')
      .then((response: AxiosResponse<Team>) => {
          context.commit('setTeam', response.data)
      })
      .catch((error: AxiosError) => {
        context.commit('setTeam', null)
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
