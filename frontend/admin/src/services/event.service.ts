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
 * Create an event. For now with default values
 */
export async function createEvent(): Promise<Event> {
  const response = await axios.post(`admin/event`, {
    name: `My new event ${Math.random()}`,
    front_page: '',
    is_open: false,
    is_visible: false,
    teams: false,
    flag_format: ''
  });
  return response.data as Event
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


