import {Challenge} from '@/models/challenge';
import axios from 'axios'
import router from '@/router';

/* API service for Challenges */

/**
 * Get all the challenges
 */
export async function getChallenges(): Promise<Challenge[]> {
  const response = await axios.get(`admin/challenges/event/${router.currentRoute.params.eventId}`);
  return response.data as Challenge[];
}

/**
 * Get a challenge by its id
 */
export async function getChallengeById(id: number): Promise<Challenge> {
  const response = await axios.get(`admin/challenges/${id}`);
  return response.data as Challenge;
}

/**
 * Delete a challenge
 * @param id Id of the challenge to delete
 * @return if the challenge was successfully deleted
 */
export async function deleteChallenge(id: number): Promise<void> {
  console.log(`deleting challenge ${id}`) // TODO: api call
}

/**
 * Create a challenge
 * @param challenge Challenge to create
 * @return if the challenge was successfully created
 */
export async function createChallenge(challenge: Challenge): Promise<void> {
  return axios.post('admin/challenges', {
    category_id: challenge.track!.id,
    description: challenge.description,
    hidden: !challenge.visible,
    name: challenge.name,
    points: challenge.points,
    flags: challenge.flags
  });
}

/**
 * Update a challenge
 * @param id Id of the challenge to update
 * @return if the challenge was successfully updated
 */
export async function updateChallenge(challenge: Challenge): Promise<void> {
  console.log(`updating challenge ${challenge.id}`); // TODO: api call
}
