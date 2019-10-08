<template>
  <div class="container is-fluid">
    <base-page-title :text="$t('title.scoreboard')" />
    <ScoreboardContainer></ScoreboardContainer>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { BasePageTitle } from '@/components'
import ScoreboardContainer from '@/components/ScoreboardContainer.vue'

export default Vue.extend({
  name: 'scoreboard',
  components: {
    BasePageTitle,
    ScoreboardContainer
  }
});
</script>
