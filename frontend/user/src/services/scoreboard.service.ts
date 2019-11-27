/**
 * API service for Scoreboard
 */
import axios from 'axios'
import { ScoreboardEntry } from '@/models/scoreboard'

/**
 * Get the scoreboard data.
 */
export async function getScoreboard(): Promise<ScoreboardEntry[]> {
  const response = await axios.get(`/scoreboard`, {data: {withEvent: true}});
  return response.data as ScoreboardEntry[]
}
