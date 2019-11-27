<template>
  <div class="teamRequestStatusModal columns is-multiline">
    <div class="column is-full requests">
      <h3><span>{{ $t('team.requestStatus') }}</span>
        <b-button @click="refreshTeam()" class="is-pulled-right" size="is-size-7" icon-right="refresh" type="is-success"></b-button>
        <div class="is-clearfix"></div>
      </h3>
      <hr>
      <b-loading :active="isFetchingTeam" :is-full-page="false"></b-loading>
      <div class="pendingRequest columns is-vcentered is-paddingless">
        <div class="column is-9">
          <div>{{ `${$t('teamName')}: ${this.request.team.name}` }}</div>
        </div>
      </div>
      <div class="pendingRequest columns is-vcentered is-paddingless">
        <div class="column is-9">
          <div>{{ `${$t('team.members')}: ${this.request.team.members.map((member) => member.participant.user.username).join(' ')}` }}</div>
        </div>
      </div>
    </div>
    <div class="column is-full leave">
      <b-button @click="cancelRequest()" size="is-small" icon-left="arrow-expand-left" type="is-danger">{{ $t('team.cancelRequest') }}</b-button>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { cancelRequest } from '@/services/team.service'
import { TeamJoinRequest } from '@/models/team_join_request'
import { sendAlert, sendAlertWithVariables } from '@/helpers'
import { FlaskRebarError } from '@/models/flask_rebar_error'
import { AxiosResponse } from 'axios'
import { TeamMixin } from '@/mixins/TeamMixin'

/**
 * Component to manage a team (either as a captain or a simple member)
 */
export default Vue.extend({
  name: 'TeamRequestStatusModal',
  mixins: [TeamMixin],
  props: {
    request: TeamJoinRequest
  },
  data() {
    return {
    }
  },
  methods: {

    /**
     * Cancel current team join request.
     */
    cancelRequest() {
      cancelRequest().then((response) => {
        sendAlert('team.requestCancelled', {type: 'is-success'})
      }).catch((error: AxiosResponse<FlaskRebarError>) => {
        sendAlertWithVariables('team.requestCancelError', {error: error.data.message})
      })
    }
  },
  components: {
  }
});
</script>

<style scoped lang="scss">
@import "../../style/theme";

/deep/ h3 .button {
  width: auto !important;
}

hr {
  margin: 0.2rem 0 1rem;
  background: $light-3;
}

.pendingRequest, .member {

  .column {
    padding-bottom: 0.25rem;
    padding-top: 0.25rem;
  }
}
</style>
