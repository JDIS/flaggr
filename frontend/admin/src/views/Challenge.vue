<template>
  <div class="is-full-height">
    <div class="page-content">
      <base-title :text="pageTitle" :color="color" />
      <div class="form">
        <b-field :label="`${$t('challenge.name')} :`">
          <b-input v-model="challenge.name"></b-input>
        </b-field>
        <b-field :label="`${$t('challenge.flag')} :`">
          <b-input v-model="challenge.flags[0].value"></b-input>
        </b-field>
        <b-field :label="`${$t('challenge.points')} :`">
          <b-input type="number" v-model="challenge.points"></b-input>
        </b-field>
        <challenge-track-input :challenge="challenge" @trackChange="updateTrack" />
        <b-field :label="`${$t('challenge.description')} :`">
          <b-input type="textarea" v-model="challenge.description"></b-input>
        </b-field>
        <challenge-tag-input v-if="false" @tagsChange="updateTags" /> <!-- hidden until supported by backend -->
      </div>

<!--      <base-subtitle :text="$t('challenge.content')" />-->
<!--      <b-field :label="`${$t('challenge.files')} :`">-->
<!--        <multiple-file-upload :color="color" @input="updateFiles" />-->
<!--      </b-field>  SAME HERE -->
    </div>
    <bottom-bar>
      <b-button :class="`is-${color}`" @click="save">{{ $t('save') }}</b-button>
      <router-link :to="{name: 'challenges'}">
        <b-button class="is-light">{{ $t('cancel') }}</b-button>
      </router-link>
    </bottom-bar>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseTitle from '../components/BaseTitle.vue';
import BaseSubtitle from '../components/BaseSubtitle.vue';
import BottomBar from '../components/BottomBar.vue';
import ChallengeTrackInput from '../components/ChallengeTrackInput.vue';
import ChallengeTagInput from '../components/ChallengeTagInput.vue';
import MultipleFileUpload from '../components/MultipleFileUpload.vue';
import {Challenge} from '../models/challenge';
import {Track} from '../models/track';
import {createChallenge, getChallengeById, updateChallenge} from '../services/challenge.service';
import {sendAlert, sendErrorAlert} from '../helpers/alerts.helper';

/**
 * Page for creating or editing a challenge
 */
export default Vue.extend({
  name: 'challenge',
  data() {
    return {
      color: 'second',
      challenge: new Challenge(),
      tags: [] as string[], // TODO: fill with existing values from API,
      name: ''
    };
  },
  async created() {
    try {
      if (this.isEditing) {
        this.challenge = await getChallengeById(this.id);
      }
    } catch (error) {
      sendErrorAlert('challenge.get.error', error);
    }
  },
  methods: {
    async save() {
      try {
        if (this.isEditing) {
          await updateChallenge(this.challenge);
        } else {
          await createChallenge(this.challenge);
        }
        sendAlert('save.success', { type: 'is-success' });
        this.$router.push({name: 'events'})
      } catch (error) {
        sendErrorAlert('save.error', error);
      }
    },
    updateFiles(newFiles: File[]) {
      this.challenge.files = newFiles;
    },
    updateTrack(selectedTrack: Track) {
      this.challenge.track = selectedTrack;
    },
    updateTags(selectedTags: string[]) {
      this.challenge.tags = selectedTags;
    }
  },
  computed: {
    id() {
      return parseInt(this.$route.params.id, 10);
    },
    isEditing() {
      return !isNaN(parseInt(this.$route.params.id, 10));
    },
    pageTitle() {
      if (this.isEditing) {
        return this.$t('challenges.edit');
      } else {
        return this.$t('challenges.create');
      }
    }
  },
  components: {
    BaseTitle,
    BaseSubtitle,
    BottomBar,
    ChallengeTrackInput,
    ChallengeTagInput,
    MultipleFileUpload
  }
});
</script>

<style lang="scss">
</style>
