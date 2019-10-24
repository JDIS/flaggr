<template>
  <section>
    <h2 class="subtitle">{{name}}</h2>
    <!-- TODO: progress chart -->
    <challenge-card
      v-for="challenge in challenges"
      v-bind:key="challenge.name"
      :challenge="challenge"
    />
  </section>
</template>

<script lang="ts">
import Vue from 'vue';
import ChallengeCard from './ChallengeCard.vue';
import { Challenge } from '../models/challenge';

/**
 * Container for a challenge track
 */
export default Vue.extend({
  name: 'TrackContainer',
  components: {
    ChallengeCard
  },
  props: {
    name: String,
    challenges: Array
  }
});
</script>

<style lang="scss" scoped>
section {
  margin: 2.5rem 0;
}

.subtitle {
  text-transform: uppercase;
}
</style>
