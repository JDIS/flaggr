import axios, { AxiosError, AxiosResponse } from 'axios'
import { Team } from '@/models/team'
import { TeamJoinRequest } from '@/models/team_join_request'
import store from '../store'


/**
 * Store to manage the connected user's team.
 */

const state = {
  userTeam: null,
  userTeamRequest: null,
}

const mutations = {
  setTeam(storeState: any, team: Team) {
    storeState.userTeam = team;
  },

  setTeamRequest(storeState: any, request: TeamJoinRequest) {
    storeState.userTeamRequest = request;
  },
}

const getters = {
  hasTeam: (storeState: any) => {
    return storeState.userTeam !== null && JSON.stringify(storeState.userTeam) !== '{}'
  },

  hasTeamRequest: (storeState: any) => {
    return storeState.userTeamRequest !== null && JSON.stringify(storeState.userTeamRequest) !== '{}'
  },
}

const actions = {
  /**
   * Fetch the team from the server and set the state accordingly.
   * If user has no team, fetch team request.
   * @param context vuex context
   */
  fetchTeam(context: any) {
    axios.get('team')
      .then((response: AxiosResponse<Team>) => {
        if (JSON.stringify(response.data) === '{}') {
          store.dispatch('team/fetchTeamRequest')
        } else {
          context.commit('setTeamRequest', null)
        }
        context.commit('setTeam', response.data)
      })
      .catch((error: AxiosError) => {
        // store.dispatch('team/fetchTeamRequest')
        context.commit('setTeam', null)
      })
  },

  /**
   * Fetch to know if the user has a pending request to join a team.
   * @param context vuex context
   */
  fetchTeamRequest(context: any) {
    axios.get('team_request')
      .then((response: AxiosResponse<TeamJoinRequest>) => {
        context.commit('setTeamRequest', response.data)
      })
      .catch((error: AxiosError) => {
        context.commit('setTeamRequest', null)
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
