<!-- team management button and modal for team management-->

<template>
  <div id="teamButtonContainer" class="is-flex is-relative">
    <b-navbar-item tag="div" @click.native="toggleTeamModalVisibility()"
                   class="has-cursor-pointer" v-if="isConnected">
      <b-tooltip :label="$t('nav.manageTeam')"
                 position="is-right" animated class="is-flex">
        <b-icon pack="mdi-light" size="is-size-3" icon="account-group"></b-icon>
      </b-tooltip>
    </b-navbar-item>
    <CustomModal v-if="teamModalShown" :visible="teamModalShown" v-on:close="toggleTeamModalVisibility()">
      <TeamModal class="connectionModalComponent"></TeamModal>
    </CustomModal>
  </div>
</template>

<script lang="ts">
  import Vue from 'vue';
  import CustomModal from '@/components/CustomModal.vue';
  import TeamModal from '@/components/TeamModal.vue';

  export default Vue.extend({
  name: 'TeamButtonContainer',
  data() {
    return {
      isConnected: true, // To change later
      teamModalShown: false
    }
  },
  methods: {
      toggleTeamModalVisibility() {
          this.teamModalShown = !this.teamModalShown
      }
  },
  components: {
    TeamModal,
    CustomModal
  }
});
</script>

<style scoped lang="scss">
@import "~bulma-helpers";
</style>
