import {Challenge} from '@/models/challenge';
import axios from 'axios'

/* API service for Challenges */

/**
 * Get all the challenges
 */
export async function getChallenges(): Promise<Challenge[]> {
  const response = await axios.get('event/0/challenges'); // TODO: get event id from backend
  const data = response.data as [];
  return data.map((challengeData: any) => createChallengeFromData(challengeData));
}

/**
 * Get a challenge by its id
 */
export async function getChallengeById(id: number): Promise<Challenge> {
  const response = await axios.get(`challenges/${id}`);
  return createChallengeFromData(response.data);
}

/**
 * Map a challenge API response data to a Challenge model
 * @param data API data corresponding to a challenge
 */
function createChallengeFromData(data: any): Challenge {
  const challenge = new Challenge();
  challenge.id = data.id;
  challenge.name = data.name;
  challenge.description = data.description;
  challenge.points = data.points;
  // TODO: set track from id (from store?)
  return challenge;
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
 * @param id Id of the challenge to create
 * @return if the challenge was successfully created
 */
export async function createChallenge(challenge: Challenge): Promise<void> {
  console.log(`creating challenge`); // TODO: api call
}

/**
 * Update a challenge
 * @param id Id of the challenge to update
 * @return if the challenge was successfully updated
 */
export async function updateChallenge(challenge: Challenge): Promise<void> {
  console.log(`updating challenge ${challenge.id}`); // TODO: api call
}
