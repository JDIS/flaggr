<template>
  <div>
    <h2 class="subtitle">{{name}}</h2>
    <!-- TODO: progress chart -->
    <challenge-card
      v-for="challenge in challenges"
      v-bind:key="challenge.name"
      :challenge="challenge"
    />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { ChallengeCard } from '../components';
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
  },
  data() {
    return {
      challenges: [
        new Challenge('On joue à cache cache?',
          'On a vu ce charmant formulaire dont on ne comprends pas trop ce qu\'il fait. On est vraiment perplexe face au fait qu\'on voit seulement un bouton, mais qu\'il y a de l\'interaction de la part du formulaire.',
          75,
          10,
          [],
          ['https://cachecache.unitedctf.ca/'],
          ['something', 'something else', 'another']),
        new Challenge('The Lost Park',
          'What is the name of this monument?',
          100,
          3,
          ['statue.jpg'],
          [],
          ['something'],
          true)
      ],

    }
  }
});
</script>

<style lang="scss">
.subtitle {
  text-transform: uppercase;
}
</style>
