<template>
  <b-collapse class="card" :open="!challenge.is_solved || newlySolved">
    <div slot="trigger" slot-scope="props" class="card-header" role="button">
      <challenge-card-header :challenge="challenge" :open="props.open" />
    </div>
    <div class="card-content">
      <challenge-card-content :challenge="challenge" @solved="addSolvedChallenge" />
    </div>
  </b-collapse>
</template>

<script lang="ts">
import Vue from 'vue'
import { Challenge } from '@/models/challenge'
import ChallengeCardHeader from './ChallengeCardHeader.vue'
import ChallengeCardContent from './ChallengeCardContent.vue'

/**
 * Card that displays a challenge
 */
export default Vue.extend({
  name: 'ChallengeCard',
  props: {
    challenge: Challenge
  },
  data() {
    return {
      newlySolved: false
    };
  },
  methods: {
    addSolvedChallenge() {
      this.newlySolved = true;
    }
  },
  components: {
    ChallengeCardHeader,
    ChallengeCardContent
  }
});
</script>

<style lang="scss">
@import "../style/theme.scss";
.card {
    margin: 2rem 0;
    border-radius: 4px;

    .card-header {
        border-radius: 4px 4px 0 0;
        padding: 0.25rem 2.5rem;
    }
    .card-content {
      font-size: 0.85rem;
      line-height: 1.5rem;
      padding: 1.5rem 2.5rem;
    }
}
</style>
