import {Event} from '@/models/event';
import store from '@/store';

/**
 * Use this mixin to have access to the event.
 */
export const EventMixin = {
  computed: {
    event(): Event {
      return (store.state as any).event.event as Event
    },

    events(): Event[] {
      return (store.state as any).event.events as Event[]
    }
  }
}
