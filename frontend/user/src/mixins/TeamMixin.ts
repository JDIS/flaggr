import store from '../store'
import { Team } from '@/models/team'
import { User } from '@/models/user'
import { TeamJoinRequest } from '@/models/team_join_request'

/**
 * Use this mixin to have access to the user's team.
 */
export const TeamMixin = {
  computed: {
    team(): Team {
      return (store.state as any).team.userTeam as Team
    },

    teamRequest(): TeamJoinRequest {
      return (store.state as any).team.userTeamRequest as TeamJoinRequest
    },

    hasPendingRequest(): boolean {
      return store.getters['team/hasTeamRequest']
    },

    hasTeam(): boolean {
      return store.getters['team/hasTeam']
    },
  },

  methods: {
    isCaptain(user: User): boolean {
      return TeamMixin.computed.hasTeam() && TeamMixin.computed.team().members.find((member) => {
        return member.user.id === user.id
      })!.captain
    }
  }
}
