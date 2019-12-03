/**
 * API service for Events
 */
import axios from 'axios'
import { Event } from '@/models/event'

/**
 * Get all the events.
 */
export async function getAllEvents(): Promise<Event[]> {
  const response = await axios.get(`event/all`);
  return response.data as Event[];
}
