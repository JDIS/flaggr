/**
 * API service for Scoreboard
 */
import axios from 'axios'
import { ScoreboardEntry } from '@/models/scoreboard'

/**
 * Get the scoreboard data.
 */
export async function getScoreboard(): Promise<ScoreboardEntry[]> {
  const response = await axios.get('event/0/scoreboard'); // TODO: get event id from url
  return response.data as ScoreboardEntry[]
}
