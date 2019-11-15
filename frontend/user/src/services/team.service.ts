/**
 * API service for Team management
 */
import axios from 'axios'
import { Team } from '@/models/team'
import store from '../store'
import { TeamJoinRequest } from '@/models/team_join_request'
import { TeamMember } from '@/models/team_member'

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
 * Refresh the team request state after.
 */
export async function sendJoinTeamRequest(id: number): Promise<Team> {
  try {
    const response = await axios.post('team_request', {team_id: id});
    store.dispatch('team/fetchTeamRequest')
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
 * Reject an invitation to join a team.
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
 * Accept an invitation to join a team.
 * Fetches the team again after completion.
 * @param request the team join request to accept
 */
export async function acceptInvitation(request: TeamJoinRequest): Promise<any> {
  try {
    const response = await axios.post('accept_team_request', {user_id: request.user.id});
    store.dispatch('team/fetchTeam')
    return response.data;
  } catch (e) {
    throw e.response
  }
}


/**
 * Toggle the role of the specified member (captain/not captain)
 * @param member the member to change role.
 */
export async function changeRole(member: TeamMember): Promise<any> {
  try {
    const response = await axios.post('change_role', {user_id: member.user.id,
                                                                captain: !member.captain});
    store.dispatch('team/fetchTeam')
    return response.data;
  } catch (e) {
    throw e.response
  }
}


/**
 * Kick a team member.
 * Fetches the team again after completion.
 * @param member Team member to kick
 */
export async function kick(member: TeamMember): Promise<any> {
  try {
    const response = await axios.post('kick_team_member', {user_id: member.user.id});
    store.dispatch('team/fetchTeam')
    return response.data;
  } catch (e) {
    throw e.response
  }
}


/**
 * Leave your current team.
 * Fetches the team again after completion.
 */
export async function leaveTeam(): Promise<any> {
  try {
    const response = await axios.post('leave_team');
    store.dispatch('team/fetchTeam')
    return response.data;
  } catch (e) {
    throw e.response
  }
}


/**
 * Cancel request to join a team
 * Fetches the requestTeam status again after completion.
 */
export async function cancelRequest(): Promise<any> {
  try {
    const response = await axios.delete('team_request');
    store.dispatch('team/fetchTeamRequest')
    return response.data;
  } catch (e) {
    throw e.response
  }
}
