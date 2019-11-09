<!-- team management button and modal for team management-->

<template>
  <div id="teamButtonContainer" class="is-flex is-relative">
    <b-navbar-item
      tag="div"
      @click.native="toggleVisibility()"
      class="has-cursor-pointer"
      v-if="isConnected"
    >
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
import CustomModal from './CustomModal.vue'
import TeamModal from './TeamModal.vue'
import FadeTransition from './FadeTransition.vue'
import { UserMixin } from '@/mixins/UserMixin'

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
  mixins: [UserMixin],
  components: {
    TeamModal,
    CustomModal,
    FadeTransition
  }
});
</script>

<style scoped lang="scss">
@import "~bulma-helpers";
</style>
