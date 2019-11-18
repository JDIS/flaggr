import {Challenge} from '../models/challenge';
import axios from 'axios'

/* API service for Challenges */

/**
 * Get all the challenges
 */
export async function getChallenges(): Promise<Challenge[]> {
  const response = await axios.get('challenges/event/1'); // TODO: get event id from backend
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
