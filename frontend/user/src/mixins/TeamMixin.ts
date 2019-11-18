import store from '../store'
import {Team} from '@/models/team'
import {TeamJoinRequest} from '@/models/team_join_request'
import {Participant} from '@/models/participant';

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
    }
  },

  methods: {
    hasTeam(): boolean {
      return store.getters['team/hasTeam']
    },

    isCaptain(participant: Participant): boolean {
      return TeamMixin.methods.hasTeam() && TeamMixin.computed.team().members.find((member) => {
        return member.participant.id === participant.id
      })!.captain
    },

    hasPendingRequest(): boolean {
      return store.getters['team/hasTeamRequest']
    }
  }
}
