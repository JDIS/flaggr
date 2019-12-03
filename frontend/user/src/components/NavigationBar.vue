<template>
  <b-navbar class="has-shadow">
    <template slot="brand">
      <b-navbar-item tag="router-link" :to="{ name: 'home' }">
        <img src="../assets/jdis_logo.png" alt="Brand logo" class="is-marginless" />
        <h1 class="title" v-if="this.event">{{ this.event.name }}</h1>
      </b-navbar-item>
    </template>
    <template slot="start">
      <navigation-bar-links />
    </template>

    <template slot="end">
      <TeamButtonContainer v-if="participant && !isSoloEvent" id="teamButtonContainer"></TeamButtonContainer>
      <div v-if="this.participant" class="participant navbar-item">{{ this.participant.user.username }}</div>
      <SignoutButton v-if="participant"></SignoutButton>
      <ConnectionButtonContainer v-else></ConnectionButtonContainer>
    </template>
  </b-navbar>
</template>

<script lang="ts">
import Vue from 'vue'
import NavigationBarLinks from '../components/NavigationBarLinks.vue'
import TeamButtonContainer from '@/components/team/TeamButtonContainer.vue'
import ConnectionButtonContainer from '@/components/ConnectionButtonContainer.vue'
import { ParticipantMixin } from '@/mixins/ParticipantMixin'
import SignoutButton from '@/components/SignoutButton.vue'
import { EventMixin } from '@/mixins/EventMixin'

export default Vue.extend({
  name: 'NavigationBar',
  mixins: [ParticipantMixin, EventMixin],
  data() {
    return {
      connectionModalShown: false,
      teamModalShown: false
    };
  },
  methods: {
    toggleConnectionModalVisibility() {
      this.connectionModalShown = !this.connectionModalShown;
    }
  },
  components: {
    NavigationBarLinks,
    TeamButtonContainer,
    ConnectionButtonContainer,
    SignoutButton
  }
});
</script>

<style scoped lang="scss">
@import "../style/theme.scss";

#teamButtonContainer {
  margin-right: 1rem;
}

.navbar-item img {
  margin-left: 1rem;
}
.title {
  font-size: 1.5rem;
  padding: 0.5rem;
}
</style>
