<template>
  <div class="teamManagementModal columns is-multiline">
    <div class="column is-full requests" v-show="this.team.requests.length > 0">
      <h3>{{ $t('team.requests') }}</h3>
      <hr>
      <div v-for="request in this.team.requests" class="pendingRequest columns is-vcentered is-paddingless">
        <div class="column is-9">
          <div>{{ request.participant.user.username }}</div>
          <div class="is-size-7 userEmail"> {{ request.participant.user.email }}</div>
        </div>
        <div v-if="isCaptain(participant)" class="column is-paddingless">
          <b-button @click="rejectInvitation(request)" size="is-small" class="button" type="is-danger" icon-right="delete"></b-button>
        </div>
        <div v-if="isCaptain(participant)" class="column is-paddingless">
          <b-button @click="acceptInvitation(request)" size="is-small" class="button" type="is-success" icon-right="check"></b-button>
        </div>
      </div>
    </div>
    <div class="column is-full members">
      <h3>{{ $t('team.members') }}</h3>
      <hr />
      <div v-for="member in this.team.members" class="member columns is-vcentered is-paddingless">
        <div class="column is-9">
          <div>
            {{ member.participant.user.username }}
            <b-icon v-if="member.captain" icon="crown" icon-pack="mdi-light" size="is-small"></b-icon>
          </div>
          <div class="is-size-7 userEmail"> {{ member.participant.email }}</div>
        </div>
        <div v-if="isCaptain(participant)" class="column is-paddingless">
          <b-button @click="kick(member)" icon-right="delete" type="is-danger" size="is-small"></b-button>
        </div>
        <div v-if="isCaptain(participant)" class="column is-paddingless">
          <b-tooltip :label="isCaptain(member.participant) ? $t('team.removeCaptain') : $t('team.makeCaptain')" v-if="member.participant.id !== participant.id">
            <b-button icon-right="crown" @click="toggleCaptain(member)" :type="isCaptain(member.participant) ? 'is-danger' : 'is-warning'" icon-pack="mdi" size="is-small"></b-button>
          </b-tooltip>
        </div>
      </div>
    </div>
    <div class="column is-full leave">
      <b-button @click="leaveTeam()" size="is-small" icon-left="arrow-expand-left" type="is-danger">{{ $t('team.leaveTeam') }}</b-button>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import {acceptInvitation, changeRole, kick, leaveTeam, rejectInvitation} from '@/services/team.service'
import {TeamMixin} from '@/mixins/TeamMixin'
import {TeamJoinRequest} from '@/models/team_join_request'
import {sendAlert, sendAlertWithVariables} from '@/helpers'
import {FlaskRebarError} from '@/models/flask_rebar_error'
import {AxiosResponse} from 'axios'
import {TeamMember} from '@/models/team_member'
import {ParticipantMixin} from '@/mixins/ParticipantMixin'

/**
 * Component to manage a team (either as a captain or a simple member)
 */
export default Vue.extend({
  name: 'TeamManagementModal',
  mixins: [ParticipantMixin, TeamMixin],
  data() {
    return {

    }
  },
  methods: {
    rejectInvitation(request: TeamJoinRequest) {
      rejectInvitation(request).then((response) => {
        sendAlertWithVariables('team.participantRejected', {participant: request.participant.user.username}, {type: 'is-success'})
      }).catch((error: AxiosResponse<FlaskRebarError>) => {
        sendAlertWithVariables('team.rejectError', {error: error.data.message})
      })
    },

    acceptInvitation(request: TeamJoinRequest) {
      acceptInvitation(request).then((response) => {
        sendAlertWithVariables('team.participantAccepted', {participant: request.participant.user.username}, {type: 'is-success'})
      }).catch((error: AxiosResponse<FlaskRebarError>) => {
        sendAlertWithVariables('team.acceptError', {error: error.data.message})
      })
    },

    /**
     * Toggles the captain role for a given participant.
     * @param member
     */
    toggleCaptain(member: TeamMember) {
      changeRole(member).then((response) => {
        sendAlertWithVariables('team.roleChanged', {participant: member.participant.user.username},
                {type: 'is-success'})
      }).catch((error: AxiosResponse<FlaskRebarError>) => {
        sendAlertWithVariables('team.roleChangeError', {error: error.data.message})
      })
    },

    /**
     * Removes a member from the team.
     * @param member The member to remove.
     */
    kick(member: TeamMember) {
      kick(member).then((response) => {
        sendAlertWithVariables('team.memberKicked', {participant: member.participant.user.username},
                {type: 'is-success'})
      }).catch((error: AxiosResponse<FlaskRebarError>) => {
        sendAlertWithVariables('team.kickError', {error: error.data.message})
      })
    },

    /**
     * Leave current team.
     */
    leaveTeam() {
      leaveTeam().then((response) => {
        sendAlert('team.leftTeam', {type: 'is-success'})
      }).catch((error: AxiosResponse<FlaskRebarError>) => {
        sendAlertWithVariables('team.leaveError', {error: error.data.message})
      })
    }
  },
  components: {
  }
});
</script>

<style scoped lang="scss">
@import "../../style/theme";

h3 {
  font-size: 110%;
}

hr {
  margin: 0.2rem 0 1rem;
  background: $light-3;
}

/deep/ .members .button, /deep/ .requests .button {
  width: auto !important;
}

.requests {
  padding-bottom: 0.6rem;
}

.userEmail {
  color: $light-2;
}

.pendingRequest, .member {

  .column {
    padding-bottom: 0.25rem;
    padding-top: 0.25rem;
  }
}

</style>
