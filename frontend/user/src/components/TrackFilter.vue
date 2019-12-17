<template>
  <section class="filter-bar">
    <b-button size="is-medium" :class="{ 'is-selected': showAll}" @click="selectAll">
      <span>{{$t('all')}}</span>
    </b-button>
    <b-button
      v-for="track in tracks"
      :key="track.id"
      size="is-medium"
      @click="toggle(track)"
      :class="{ 'is-selected': !showAll && isSelected(track)}"
    >{{track.name}}</b-button>
  </section>
</template>

<script lang="ts">
import Vue from 'vue'
import { Track } from '@/models/track'

/**
 * Filter which tracks to show in the list
 */
export default Vue.extend({
  name: 'TrackFilter',
  components: {},
  props: {
    tracks: {
      type: Array as () => Track[]
    }
  },
  data() {
    return {
      visibleTracks: [] as Track[],
      showAll: true
    };
  },
  watch: {
    // Select all tracks when list is initialized
    tracks(tracks) {
      this.visibleTracks = tracks;
      this.onChange();
    }
  },
  methods: {
    /**
     * Called when client selects or deselects tracks. If no tracks are selected,
     * select all tracks.
     */
    onChange() {
      if (this.visibleTracks.length === 0) {
        this.selectAll()
      }
      this.$emit('change', this.visibleTracks);
    },

    toggle(track: Track) {
      // Clear visibleTracks when 'all' was selected before and add only this track
      if (this.showAll) {
        this.visibleTracks = [track];
        this.showAll = false;
      } else if (this.isSelected(track)) {
        // Remove track from selected list if it was already selected
        this.visibleTracks = this.visibleTracks.filter((x) => x !== track);
      } else {
        // Add track to selected list
        this.visibleTracks.push(track);
      }
      this.onChange();
    },

    selectAll(): void {
      this.showAll = true;
      this.visibleTracks = this.tracks;
      if (this.visibleTracks.length > 1) {
        this.onChange();
      }
    },

    isSelected(track: Track): boolean {
      return this.visibleTracks.includes(track);
    }
  },
  computed: {}
});
</script>

<style lang="scss">
@import "../plugins/buefy-theme.scss";

.filter-bar {
  width: 100%;
  background-color: $grey-darker;
  border-radius: 0.3rem;
  display: flex;
      
    .button {
      min-width: 6rem;
      width: auto;
      background-color: $grey-darker;
      color: $light-0;
      border: none;
      border-radius: 0;

      span {
        font-weight: 300;
      }
      
      &:first-child {
        border-top-left-radius: 0.3rem;
        border-bottom-left-radius: 0.3rem;
      }

      &:hover, &.is-selected {
        background-color: $black-bis;
        border-bottom: 2px $secondary-color solid;
      }

      &.is-selected span {
        font-weight: 600;
      }
  }
}

</style>
