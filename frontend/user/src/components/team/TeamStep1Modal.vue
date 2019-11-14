<template>
  <div class="teamModal">
    <b-field :label="$t('teamManagement')" custom-class="has-text-centered is-medium"></b-field>
    <div id="top" class="columns">
      <div
        class="column text is-two-fifths"
        :class="{ active: !isJoinTeam }"
        id="create"
        @click="focusCreateTeam()"
      >{{ $t('create') }}</div>
      <b-switch
        class="column is-flex is-one-fifth"
        id="switch"
        v-model="isJoinTeam"
        :rounded="false"
      ></b-switch>
      <div
        class="column text is-two-fifths has-text-right"
        :class="{ active: isJoinTeam }"
        id="join"
        @click="focusJoinTeam()"
      >{{ $t('join') }}</div>
    </div>
    <div id="form">
      <b-field
        :label="$t('teamName')"
        custom-class="is-size-7"
        v-if="!isJoinTeam"
        label-for="teamName"
      >
        <b-input
          placeholder="TheBestTeam"
          expanded
          v-model="teamName"
          id="teamName"
          icon="account-group"
        ></b-input>
      </b-field>
      <b-field
        :label="$t('teamToJoin')"
        custom-class="is-size-7"
        v-if="isJoinTeam"
        label-for="teamToJoin"
      >
        <b-select
          expanded
          v-model="teamToJoin"
          id="teamToJoin"
          icon="account-group"
        >
          <option
            class="has-text-light"
            v-for="team in teams"
            :value="team"
            :key="team.id"
          >{{ team.name }}</option>
        </b-select>
      </b-field>
      <b-button
        type="is-primary"
        size="is-medium"
        @click="onSubmit()"
        :disabled="!canSubmit()"
        :icon-right="isJoinTeam ? 'arrow-right' : 'plus-box'"
      >{{ $t(isJoinTeam ? 'joinTeam' : 'createTeam') }}</b-button>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { createTeam, fetchTeams, sendJoinTeamRequest } from '@/services/team.service'
import { sendAlert, sendAlertWithVariables } from '@/helpers'
import { AxiosResponse } from 'axios'
import { FlaskRebarError } from '@/models/flask_rebar_error'
import { Team } from '@/models/team'

/**
 * Modal to create or join a team as a user.
 */
export default Vue.extend({
  name: 'TeamStep1Modal',
  data() {
    return {
      isJoinTeam: true,
      teamName: '',
      teamToJoin: null as (null | Team),
      teams: [] as Team[],
    }
  },
  mounted() {
    fetchTeams().then((teams) => {
      this.teams = teams
    })
  },
  methods: {
    focusCreateTeam() {
      this.isJoinTeam = false
    },

    focusJoinTeam() {
      this.isJoinTeam = true
    },

    onSubmit() {
      if (this.isJoinTeam) {
        if (this.teamToJoin) {
          sendJoinTeamRequest(this.teamToJoin.id).then((response) => {
            sendAlert('team.sendJoinRequestSent', {type: 'is-success'})
          }).catch((error: AxiosResponse<FlaskRebarError>) => {
            sendAlertWithVariables('team.sendJoinRequestError', {error: error.data.message})
          })
        }
      } else {
        createTeam(this.teamName).then((team) => {
          sendAlertWithVariables('team.creationSuccessful', {team: team.name}, {type: 'is-success'})
        }).catch((error: AxiosResponse<FlaskRebarError>) => {
          sendAlertWithVariables('team.creationError', {error: error.data.message})
        })
      }
    },

    canSubmit() {
      return (this.isJoinTeam && this.teamToJoin !== null) || (!this.isJoinTeam && this.teamName.trim() !== '')
    }
  },
  components: {
  }
});
</script>

<style scoped lang="scss">
@import "../../style/theme";

#top {
  #switch {
    justify-content: center;
  }

  .active {
    color: $primary-color-light;
    text-decoration: underline;
  }

  .text {
    font-size: 1.2rem;
    cursor: pointer;
  }

  #connection {
    text-align: left;
  }

  #signUp {
    text-align: right;
  }
}
</style>
