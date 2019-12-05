import {Event} from '@/models/event';
import axios from 'axios'

/* API service for Events */

/**
 * Get all the events
 */
export async function getEvents(): Promise<Event[]> {
  const response = await axios.get('event/all');
  return response.data
}
