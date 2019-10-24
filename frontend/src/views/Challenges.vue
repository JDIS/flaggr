<template>
  <div class="container is-fluid">
    <base-page-title :text="$t('title.challenges')" />
    <track-filter :tracks="['web', 'crypto']" @change="updateTracks" />
    <track-container
      v-for="track in tracks"
      :key="track"
      :name="track"
      :challenges="getTrackChallenges(track)"
    />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BasePageTitle from '../components/base/BasePageTitle.vue';
import TrackFilter from '../components/TrackFilter.vue';
import TrackContainer from '../components/TrackContainer.vue';
import { Challenge } from '../models/challenge';
import { getChallenges } from '../services/challenge.service';

/**
 * Challenges page
 */
export default Vue.extend({
  name: 'challenges',
  components: {
    BasePageTitle,
    TrackFilter,
    TrackContainer
  },
  data() {
    return {
      tracks: [] as string[],
      challenges: [] as Challenge[]
    };
  },
  created() {
    this.challenges = getChallenges();
  },
  methods: {
    updateTracks(tracks: string[]): void {
      this.tracks = tracks;
    },
    getTrackChallenges(track: string): Challenge[] {
      return this.challenges.filter((challenge) => challenge.track === track);
    }
  }
});
</script>
