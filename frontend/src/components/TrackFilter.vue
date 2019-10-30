<template>
  <section class="filter-bar">
    <b-button size="is-medium" :class="{ 'is-selected': showAll}" @click="selectAll">
      <span>{{$t('all')}}</span>
    </b-button>
    <b-button
      v-for="track in tracks"
      :key="track"
      size="is-medium"
      @click="toggle(track)"
      :class="{ 'is-selected': !showAll && isSelected(track)}"
    >{{track}}</b-button>
  </section>
</template>

<script lang="ts">
import Vue from 'vue';

/**
 * Filter which tracks to show in the list
 */
export default Vue.extend({
  name: 'TrackFilter',
  components: {},
  props: {},
  data() {
    return {
      tracks: [] as string[],
      visibleTracks: [] as string[],
      showAll: true
    };
  },
  created() {
    this.tracks = this.getTracks();
    this.visibleTracks = this.tracks;
    this.onChange();
  },
  methods: {
    getTracks(): string[] {
      return ['web', 'crypto']; // TODO: get from API or parent component
    },

    onChange() {
      this.$emit('change', this.visibleTracks);
    },

    toggle(track: string) {
      // Deselect everything except the track when 'all' was selected before
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
      this.onChange();
    },

    isSelected(track: string): boolean {
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
