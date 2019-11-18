import axios, { AxiosError, AxiosResponse } from 'axios'
import { Team } from '@/models/team'
import { TeamJoinRequest } from '@/models/team_join_request'
import store from '../store'


/**
 * Store to manage the connected participant's team.
 */

const state = {
  participantTeam: null,
  participantTeamRequest: null,
}

const mutations = {
  setTeam(storeState: any, team: Team) {
    storeState.participantTeam = team;
  },

  setTeamRequest(storeState: any, request: TeamJoinRequest) {
    storeState.participantTeamRequest = request;
  },
}

const getters = {
  hasTeam: (storeState: any) => {
    return storeState.participantTeam !== null && JSON.stringify(storeState.participantTeam) !== '{}'
  },

  hasTeamRequest: (storeState: any) => {
    return storeState.participantTeamRequest !== null && JSON.stringify(storeState.participantTeamRequest) !== '{}'
  },
}

const actions = {
  /**
   * Fetch the team from the server and set the state accordingly.
   * If participant has no team, fetch team request.
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
        context.commit('setTeam', null)
      })
  },

  /**
   * Fetch to know if the participant has a pending request to join a team.
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
