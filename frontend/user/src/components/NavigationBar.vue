<template>
  <b-navbar class="has-shadow">
    <template slot="brand">
      <b-navbar-item tag="router-link" :to="{ path: '/' }">
        <img src="../assets/jdis_logo.svg" alt="Brand logo" class="is-marginless" />
        <h1 class="title">{{ $t('projectName')}}</h1>
      </b-navbar-item>
    </template>
    <template slot="start">
      <navigation-bar-links />
    </template>

    <template slot="end">
      <TeamButtonContainer v-if="user" id="teamButtonContainer"></TeamButtonContainer>
      <div v-if="this.user" class="user navbar-item">{{ this.user.username }}</div>
      <SignoutButton v-if="user"></SignoutButton>
      <ConnectionButtonContainer v-else></ConnectionButtonContainer>
    </template>
  </b-navbar>
</template>

<script lang="ts">
import Vue from 'vue'
import NavigationBarLinks from '../components/NavigationBarLinks.vue'
import TeamButtonContainer from '@/components/team/TeamButtonContainer.vue'
import ConnectionButtonContainer from '@/components/ConnectionButtonContainer.vue'
import { UserMixin } from '@/mixins/UserMixin'
import SignoutButton from '@/components/SignoutButton.vue'

export default Vue.extend({
  name: 'NavigationBar',
  mixins: [UserMixin],
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
