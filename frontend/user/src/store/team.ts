import axios, { AxiosError, AxiosResponse } from 'axios'
import { Team } from '@/models/team'
import { TeamJoinRequest } from '@/models/team_join_request'
import store from '../store'
import route from '@/router'


/**
 * Store to manage the connected participant's team.
 */

const state = {
  participantTeam: null,
  participantTeamRequest: null,
  isFetchingTeam: false
}

const mutations = {
  setTeam(storeState: any, team: Team) {
    storeState.participantTeam = team;
  },

  setTeamRequest(storeState: any, request: TeamJoinRequest) {
    storeState.participantTeamRequest = request;
  },

  setFetchingTeam(storeState: any, fetching: boolean) {
    storeState.isFetchingTeam = fetching;
  },
}

const getters = {
  hasTeam: (storeState: any) => {
    return storeState.participantTeam !== null && JSON.stringify(storeState.participantTeam) !== '{}'
  },

  hasTeamRequest: (storeState: any) => {
    return storeState.participantTeamRequest !== null && JSON.stringify(storeState.participantTeamRequest) !== '{}'
  },

  isFetchingTeam: (storeState: any) =>  {
    return storeState.isFetchingTeam
  }
}

/**
 * If the current route requires a team, redirect to home.
 * This function should only be called if we know the client
 * is connected.
 */
function checkPermissions() {
  if (route.currentRoute.meta.requiresTeam === true) {
    route.push(`/${route.currentRoute.params.eventId}`)
  }
}

const actions = {
  /**
   * Fetch the team from the server and set the state accordingly.
   * If user has no team, fetch team request.
   * @param context vuex context
   */
  fetchTeam(context: any) {
    context.commit('setFetchingTeam', true)
    axios.get('team')
      .then((response: AxiosResponse<Team>) => {
        if (JSON.stringify(response.data) === '{}') {
          store.dispatch('team/fetchTeamRequest')
          checkPermissions()
        } else {
          context.commit('setTeamRequest', null)
          context.commit('setFetchingTeam', false)
        }
        context.commit('setTeam', response.data)
      })
      .catch((error: AxiosError) => {
        context.commit('setTeam', null)
        checkPermissions()
        context.commit('setFetchingTeam', false)
      })
  },

  /**
   * Fetch to know if the participant has a pending request to join a team.
   * @param context vuex context
   */
  fetchTeamRequest(context: any) {
    context.commit('setFetchingTeam', true)
    axios.get('team_request')
      .then((response: AxiosResponse<TeamJoinRequest>) => {
        context.commit('setTeamRequest', response.data)
      })
      .catch((error: AxiosError) => {
        context.commit('setTeamRequest', null)
      })
      .finally(() => context.commit('setFetchingTeam', false))
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
}
