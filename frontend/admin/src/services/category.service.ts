import axios from 'axios'
import {Track} from '@/models/track';

/* API service for Categories (tracks) */

/**
 * Get all the categories for an event
 */
export async function getCategories(eventId: string): Promise<Track[]> {
  const response = await axios.get(`admin/categories/event/${eventId}`);
  return response.data as Track[];
}

/**
 * Create a new category for an event
 */
export async function createCategory(category: Track, eventId: string): Promise<Track> {
  const response = await axios.post(`admin/categories`, {event_id: eventId, name: category.name});
  return response.data as Track;
}
