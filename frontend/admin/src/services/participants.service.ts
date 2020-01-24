import axios from 'axios'
import {Participant} from '@/models/participant';

/* API service for Participants */

/**
 * Get all participants for a given event
 */
export async function getParticipants(eventId: string): Promise<Participant[]> {
  const response = await axios.get(`admin/event/${eventId}/participants`);
  return response.data
}
