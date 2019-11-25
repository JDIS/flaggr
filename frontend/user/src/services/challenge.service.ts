/**
 * API service for Challenges
 */
import { Challenge } from '@/models/challenge'
import { Track } from '@/models/track'
import axios from 'axios'

/**
 * Get all the challenges grouped by track. Places solved challenges last in the
 * list.
 */
export async function getChallengesByTrack(): Promise<Track[]> {
  const response = await axios.get('challenges/event/0/by-category'); // TODO: get event id from backend
  const data = response.data as [];
  const tracks: Track[] = data.map((trackData: any) => createTrackFromData(trackData))
  tracks.forEach((track) => {
    track.challenges.sort((challenge1, challenge2) => challenge1.is_solved ? 1 : -1)
  })
  return tracks;
}

/**
 * Map a track API response data to a Track model
 * @param data API data corresponding to a track
 */
function createTrackFromData(data: any): Track {
  const challenges = data.challenges.map((challengeData: any) => createChallengeFromData(challengeData));
  return new Track(data.id, data.name, challenges);
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
  challenge.is_solved = data.is_solved;
  challenge.solves = data.solves;
  return challenge;
}

/**
 * Submit a flag for a challenge.
 * @param challengeId Id of the challenge we're submitting an answer for
 * @param flag The answer to the challenge
 */
export async function submitFlag(challengeId: number, flag: string): Promise<boolean> {
  try {
    const response = await axios.post(`challenges/${challengeId}/submit`,
      {flag: flag})
    return response.data.correct
  } catch (e) {
    throw e.response
  }
}
