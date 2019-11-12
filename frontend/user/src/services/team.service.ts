/**
 * API service for Team management
 */
import axios from 'axios'
import { Team } from '@/models/team'
import store from '../store'
import { TeamJoinRequest } from '@/models/team_join_request'

/**
 * Send a request to create a team. If an error occurs, throw it.
 */
export async function createTeam(name: string): Promise<Team> {
  try {
    const response = await axios.post('team', {name: name});
    store.dispatch('team/fetchTeam')
    return response.data;
  } catch (e) {
    throw e.response
  }
}

/**
 * Send a request to join a team. If an error occurs, throw it.
 */
export async function sendJoinTeamRequest(id: number): Promise<Team> {
  try {
    const response = await axios.post('team_request', {team_id: id});
    return response.data;
  } catch (e) {
    throw e.response
  }
}


/**
 * Get the list of teams for the event.
 */
export async function fetchTeams(): Promise<Team[]> {
  try {
    const response = await axios.get('teams');
    return response.data;
  } catch (e) {
    throw e.response
  }
}


/**
 * Reject an invitation to join a team. Only team captains can do it.
 * Fetches the team again after completion.
 * @param request the team join request to reject
 */
export async function rejectInvitation(request: TeamJoinRequest): Promise<any> {
  try {
    const response = await axios.post('decline_team_request', {user_id: request.user.id});
    store.dispatch('team/fetchTeam')
    return response.data;
  } catch (e) {
    throw e.response
  }
}


/**
 * Accept an invitation to join a team. Only team captains can do it.
 * Fetches the team again after completion.
 * @param request the team join request to accept
 */
export async function acceptInvitation(request: TeamJoinRequest): Promise<any> {
  try {
    console.log('request', request.user.id)
    const response = await axios.post('accept_team_request', {user_id: request.user.id});
    store.dispatch('team/fetchTeam')
    return response.data;
  } catch (e) {
    throw e.response
  }
}
