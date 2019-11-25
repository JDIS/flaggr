<!-- team management button and modal for team management-->

<template>
  <div id="teamButtonContainer" class="is-flex is-relative">
    <b-navbar-item
      tag="div"
      @click.native="toggleVisibility()"
      class="has-cursor-pointer"
      v-if="isConnected()"
    >
      <div v-if="hasTeam && isCaptain(participant)" v-show="team.requests.length > 0" class="has-text-warning notification">{{ team.requests.length}}</div>
      <div v-if="hasPendingRequest" class="has-text-warning notification">...</div>
      <b-tooltip :label="$t('nav.manageTeam')" position="is-right" animated class="is-flex">
        <b-icon pack="mdi-light" size="is-size-3" icon="account-group"></b-icon>
      </b-tooltip>
    </b-navbar-item>
    <FadeTransition>
      <CustomModal v-if="shown" :visible="shown" v-on:close="toggleVisibility()">
        <TeamModal class="connectionModalComponent"></TeamModal>
      </CustomModal>
    </FadeTransition>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import CustomModal from '../CustomModal.vue'
import TeamModal from './TeamModal.vue'
import FadeTransition from '../FadeTransition.vue'
import {ParticipantMixin} from '@/mixins/ParticipantMixin'
import {TeamMixin} from '@/mixins/TeamMixin'

export default Vue.extend({
  name: 'TeamButtonContainer',
  data() {
    return {
      shown: false
    };
  },
  methods: {
    toggleVisibility() {
      this.shown = !this.shown;
    }
  },
  mixins: [ParticipantMixin, TeamMixin],
  components: {
    TeamModal,
    CustomModal,
    FadeTransition
  }
});
</script>

<style scoped lang="scss">

.notification {
  display: block;
  position: absolute;
  text-align: center;
  font-weight: bolder;
  width: 1rem;
  height: 1rem;
  top:0.4rem;
  right:0;
  z-index: 10;
  margin:0;
  padding: 0;
  background: transparent;
}
</style>
