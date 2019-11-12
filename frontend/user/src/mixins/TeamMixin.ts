import store from '../store'
import { Team } from '@/models/team'

/**
 * Use this mixin to have access to the user's team.
 */
export const TeamMixin = {
  computed: {
    team(): Team {
      return (store.state as any).team.userTeam as Team
    },

    hasTeam(): boolean {
      return store.getters['team/hasTeam']
    }
  }
}
