import store from '../store'
import { Event } from '@/models/event'

/**
 * Use this mixin to have access to the event.
 */
export const EventMixin = {
  computed: {
    event(): Event {
      return (store.state as any).event.event as Event
    },

    hasEvent(): boolean {
      return store.getters['event/hasEvent']
    },
  }
}
