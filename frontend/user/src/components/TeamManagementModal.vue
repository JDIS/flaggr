<template>
  <div class="teamManagementModal container">
    <div class="requests" v-show="this.team.requests.length > 0">
      <h3>{{ $t('team.requests') }}</h3>
      <hr>
      <div v-for="request in this.team.requests" class="pendingRequest columns is-vcentered">
        <div class="column is-8">
          <div>{{ request.user.username }}</div>
          <div class="is-size-7 userEmail"> {{ request.user.email }}</div>
        </div>
        <div class="column">
          <b-button @click="rejectInvitation(request)" class="button" type="is-danger" icon-right="delete"></b-button>
        </div>
        <div class="column">
          <b-button @click="acceptInvitation(request)" class="button" type="is-success" icon-right="check"></b-button>
        </div>
      </div>
    </div>
    <div class="members">
      <h3>{{ $t('team.members') }}</h3>
      <hr />
      <div v-for="member in this.team.members">{{ member.user.username }}</div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue"
import { acceptInvitation, rejectInvitation } from "@/services/team.service"
import { TeamMixin } from "@/mixins/TeamMixin"
import { TeamJoinRequest } from "@/models/team_join_request"
import { sendAlertWithVariables } from "@/helpers"
import { FlaskRebarError } from "@/models/flask_rebar_error"
import { AxiosResponse } from "axios"

/**
 * Component to manage a team (either as a captain or a simple member)
 */
export default Vue.extend({
  name: 'TeamManagementModal',
  mixins: [TeamMixin],
  data() {
    return {

    }
  },
  methods: {
    rejectInvitation(request: TeamJoinRequest) {
      rejectInvitation(request).then((response) => {
        sendAlertWithVariables('team.userRejected', {user: request.user.username}, {type: 'is-success'})
      }).catch((error: AxiosResponse<FlaskRebarError>) => {
        sendAlertWithVariables('team.rejectError', {error: error.data.message})
      })
    },

    acceptInvitation(request: TeamJoinRequest) {
      acceptInvitation(request).then((response) => {
        sendAlertWithVariables('team.userAccepted', {user: request.user.username}, {type: 'is-success'})
      }).catch((error: AxiosResponse<FlaskRebarError>) => {
        sendAlertWithVariables('team.acceptError', {error: error.data.message})
      })
    }
  },
  components: {
  }
});
</script>

<style scoped lang="scss">
@import "../style/theme.scss";

h3 {
  font-size: 110%;
}

hr {
  margin: 0.2rem 0 0.5rem;
  background: $light-3;
}

/deep/ .button {
  width: auto !important;
}

.pendingRequest {
  padding: 0.4rem 0 0.8rem;

  .userEmail {
    color: $light-2;
  }
}
</style>
