<template>
  <div class="container is-fluid">
    <base-page-title :text="$t('title.challenges')" />
    <track-filter :tracks="tracks" @change="updateVisibleTracks" />
    <track-container
      v-for="track in visibleTracks"
      :key="track.id"
      :name="track.name"
      :challenges="track.challenges"
    />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BasePageTitle from '../components/base/BasePageTitle.vue';
import TrackFilter from '../components/TrackFilter.vue';
import TrackContainer from '../components/TrackContainer.vue';
import { Challenge } from '../models/challenge';
import { Track } from '../models/track';
import { getChallengesByTrack } from '../services/challenge.service';

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
      tracks: [] as Track[],
      visibleTracks: [] as Track[],
      challenges: [] as Challenge[]
    };
  },
  async created() {
    this.tracks = await getChallengesByTrack();
  },
  methods: {
    updateVisibleTracks(visibleTracks: Track[]) {
      this.visibleTracks = visibleTracks;
    }
  }
});
</script>
