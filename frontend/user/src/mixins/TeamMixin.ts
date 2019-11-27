import store from '../store'
import { Team } from '@/models/team'
import { Participant } from '@/models/participant'
import { TeamJoinRequest } from '@/models/team_join_request'

/**
 * Use this mixin to have access to the participant's team.
 */
export const TeamMixin = {
  computed: {
    team(): Team {
      return (store.state as any).team.participantTeam as Team
    },

    teamRequest(): TeamJoinRequest {
      return (store.state as any).team.participantTeamRequest as TeamJoinRequest
    },

    isFetchingTeam(): boolean {
      return store.getters['team/isFetchingTeam']
    },

    hasPendingRequest(): boolean {
      return store.getters['team/hasTeamRequest']
    },

    hasTeam(): boolean {
      return store.getters['team/hasTeam']
    },
  },

  methods: {
    isCaptain(participant: Participant): boolean {
      return TeamMixin.computed.hasTeam() && TeamMixin.computed.team().members.find((member) => {
        return member.participant.id === participant.id
      })!.captain
    },

    refreshTeam() {
      store.dispatch('team/fetchTeam')
    },
  }
}
