import {Event} from '@/models/event';
import axios from 'axios'

/* API service for Events */

/**
 * Get all the events
 */
export async function getEvents(): Promise<Event[]> {
  const response = await axios.get('admin/event/all');
  return response.data
}

/**
 * Get an event
 * @param id of the event
 */
export async function getEvent(id: string): Promise<Event> {
  const response = await axios.get(`admin/event/${id}`);
  return response.data
}

/**
 * Edit an event.
 * @param event The new event data
 * @param id The id of the event
 */
export async function editEvent(event: Event, id: string): Promise<Event> {
  const response = await axios.put(`admin/event/${id}`, event);
  return response.data as Event
}


