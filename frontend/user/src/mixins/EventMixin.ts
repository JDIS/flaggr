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

    /**
     * True if the event is not a team event.
     */
    isSoloEvent(): boolean {
      const event = (store.state as any).event.event as Event
      return event && !event.teams
    }
  }
}
