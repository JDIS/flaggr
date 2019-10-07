<template>
  <div class="container is-fluid">
    <base-page-title :text="$t('title.challenges')" />
    <!-- TODO: Track filter -->
    <track-container name="Web" />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { BasePageTitle, TrackContainer } from '../components';

/**
 * Challenges page
 */
export default Vue.extend({
  name: 'challenges',
  components: {
    BasePageTitle,
    TrackContainer
  },
});
</script>
