<template>
  <div class="is-full-height">
    <div class="page-content">
      <base-title :text="pageTitle" :color="color" />
      <div class="form">
        <b-field :label="`${$t('challenge.name')} :`">
          <b-input v-model="challenge.name"></b-input>
        </b-field>
        <b-field :label="`${$t('challenge.flag')} :`">
          <b-input v-model="challenge.flag"></b-input>
        </b-field>
        <b-field :label="`${$t('challenge.points')} :`">
          <b-input type="number" v-model="challenge.points"></b-input>
        </b-field>
        <b-field :label="`${$t('challenge.description')} :`">
          <b-input type="textarea" v-model="challenge.description"></b-input>
        </b-field>
      </div>
    </div>
    <bottom-bar>
      <b-button :class="`is-${color}`" @click="save">{{ $t('save') }}</b-button>
      <router-link to="/challenges">
        <b-button class="is-light">{{ $t('cancel') }}</b-button>
      </router-link>
    </bottom-bar>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseTitle from '../components/BaseTitle.vue';
import BottomBar from '../components/BottomBar.vue';
import { Challenge } from '../models/challenge';
import {
  getChallengeById,
  createChallenge,
  updateChallenge
} from '../services/challenge.service';
import { sendAlert, sendErrorAlert } from '../helpers/alerts.helper';

/**
 * Page for creating or editing a challenge
 */
export default Vue.extend({
  name: 'challenge',
  data() {
    return {
      color: 'second',
      challenge: new Challenge()
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
        sendAlert('save.success', { type: 'is-success'});
      } catch (error) {
        sendErrorAlert('save.error', error);
      }
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
    BottomBar
  }
});
</script>

<style lang="scss">
.form {
  margin-top: 1rem;
}
</style>