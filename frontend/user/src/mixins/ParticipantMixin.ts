import {Participant} from '@/models/participant'
import store from '../store'

/**
 * Use this mixin to have access to the connected participant.
 */
export const ParticipantMixin = {
  computed: {
    participant(): Participant {
      return (store.state as any).participant.connectedParticipant as Participant
    }
  },

  methods: {
    isConnected(): boolean {
      return store.getters['participant/isConnected']
    }
  }
}
