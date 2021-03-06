<template>
  <b-field :label="`${$t('challenge.track')} :`" class="track-field">
    <b-autocomplete
      v-model="currentInput"
      field="name"
      ref="autocomplete"
      open-on-focus
      :data="filteredTracks"
      @select="changeTrack"
      @focus="currentInput = ''"
    >
      <template slot="footer">
        <a class="dropdown-item" @click="showAddTrackDialog">
          <b-icon icon="plus-circle" size="is-small"></b-icon>
          <span>{{$t('track.create')}}</span>
        </a>
      </template>
      <template slot="empty">
        <span class="dropdown-item">{{$t('noresult', { value: currentInput })}}</span>
      </template>
    </b-autocomplete>
  </b-field>
</template>

<script lang="ts">
import Vue from 'vue';
import {Track} from '@/models/track';
import {createCategory, getCategories} from '@/services/category.service';
import {sendErrorAlert} from '@/helpers/alerts.helper';

/**
 * Input for choosing a track from existing list or add new ones
 */
export default Vue.extend({
  name: 'ChallengeTrackInput',
  props: {
    challenge: Object
  },
  data() {
    return {
      tracks: [] as Track[],
      selectedTrack: {} as Track,
      selectedName: '',
      currentInput: ''
    };
  },
  watch: {
    challenge(newVal, oldVal) {
      this.selectedTrack = newVal.category
      this.selectedName = newVal.category.name
      this.currentInput = newVal.category.name
    }
  },
  created() {
    getCategories(this.$route.params.eventId)
        .then((categories) => this.tracks = categories)
        .catch((error) => {
          sendErrorAlert('categories.get.error', error);
        })
  },
  methods: {
    isInTrackList(name: string) {
      return this.tracks.some((track) => {
        return track.name === name;
      });
    },
    changeTrack(option: Track) {
      if (option) {
        this.selectedTrack = option;
        this.selectedName = option.name;
        this.$emit('trackChange', this.selectedTrack);
      }
    },
    /** Displays a dialog to create a new track and select it */
    showAddTrackDialog() {
      this.$buefy.dialog.prompt({
        message: this.$t('track.create').toString(),
        inputAttrs: {
          value: this.isInTrackList(this.currentInput) ? '' : this.currentInput
        },
        confirmText: this.$t('create').toString(),
        cancelText: this.$t('cancel').toString(),
        onConfirm: (value: string) => {
          const newTrack = new Track(3, value);
          createCategory(newTrack, this.$route.params.eventId)
            .then((category) => {
              this.tracks.push(category);
              (this.$refs.autocomplete as any).setSelected(category.name); // Calls b-autocomplete method setSelected
              this.changeTrack(category);
            })
            .catch((error) => sendErrorAlert('category.create.error', error))
        },
        onCancel: () => {
          if (this.selectedName) {
            (this.$refs.autocomplete as any).setSelected(
              this.selectedTrack.name
            );
          }
        }
      });
    }
  },
  computed: {
    /* Return tracks that contains the current user input */
    filteredTracks(): Track[] {
      return this.tracks.filter((track) => {
        return (
          track.name.toLowerCase().indexOf(this.currentInput.toLowerCase()) >= 0
        );
      });
    }
  }
});
</script>

<style lang="scss">
.track-field div.dropdown-item {
  padding: 0!important;

  .icon {
    margin-right: 0.25rem;
  }
  span {
    font-weight: 600;
  }
}
</style>
