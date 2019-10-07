<!-- Modal to create or join a team as a user. -->

<template>
  <div class="teamModal">
    <b-field :label="$t('teamManagement')" custom-class="has-text-centered is-medium"></b-field>
    <div id="top" class="columns">
      <div
        class="column text is-two-fifths"
        :class="{ active: !isInscription }"
        id="create"
        @click="focusCreateTeam()"
      >{{ $t('create') }}</div>
      <b-switch
        class="column is-flex is-one-fifth"
        id="switch"
        v-model="isInscription"
        :rounded="false"
      ></b-switch>
      <div
        class="column text is-two-fifths has-text-right"
        :class="{ active: isInscription }"
        id="join"
        @click="focusJoinTeam()"
      >{{ $t('join') }}</div>
    </div>
    <div id="form">
      <b-field
        :label="$t('teamName')"
        custom-class="is-size-7"
        v-if="!isInscription"
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
        v-if="isInscription"
        label-for="teamToJoin"
      >
        <b-select
          placeholder="TheBestTeam"
          expanded
          v-model="teamToJoin"
          id="teamToJoin"
          icon="account-group"
        >
          <option
            class="has-text-light"
            v-for="option in teams"
            :value="option"
            :key="option"
          >{{ option }}</option>
        </b-select>
      </b-field>
      <b-button
        type="is-primary"
        size="is-medium"
        :icon-right="isInscription ? 'arrow-right' : 'plus-box'"
      >{{ $t(isInscription ? 'joinTeam' : 'createTeam') }}</b-button>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'ConnectionModal',
  data() {
    return {
      isInscription: true,
      teamName: '',
      teamToJoin: '',
      teams: ['mocked', 'teams', 'to', 'join'],
    }
  },
  methods: {
    focusCreateTeam() {
      this.isInscription = false
    },

    focusJoinTeam() {
      this.isInscription = true
    }
  },
  components: {
  }
});
</script>

<style scoped lang="scss">
@import "../style/theme.scss";

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
