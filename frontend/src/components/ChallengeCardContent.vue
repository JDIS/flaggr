<template>
  <div class="columns">
    <div class="column is-three-quarters">
      <div class="solves">{{$t('challenge.solves', { number: challenge.solves })}}</div>
      <div class="description">{{ challenge.description }}</div>
      <div class="files">
        <a v-for="file in challenge.files" v-bind:key="file">
          <b-icon icon="download" size="is-small"></b-icon>
          {{ file }}
        </a>
      </div>
      <div class="url">
        <a v-for="link in challenge.links" v-bind:key="link">
          <b-icon icon="open-in-new" size="is-small"></b-icon>
          {{link}}
        </a>
      </div>
      <div class="submission">
        <b-field>
          <b-input placeholder="FLAG-ThisIsAnExampl3" expanded></b-input>
          <p class="control">
            <b-button class="button is-primary">{{$t('submit')}}</b-button>
          </p>
        </b-field>
      </div>
    </div>
    <div class="column">
      <b-taglist>
        <b-tag v-for="tag in challenge.tags" v-bind:key="tag">{{tag}}</b-tag>
      </b-taglist>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { Challenge } from '../models/challenge';

/**
 * Content of the challenge card
 */
export default Vue.extend({
  name: 'ChallengeCardContent',
  props: {
    challenge: Challenge
  },
  components: {
  }
});
</script>

<style lang="scss">
@import "@/style/theme.scss";

.solves {
    margin-bottom: 0.5rem;
    color: $light-3;
}
.description {
    font-weight: 300;
}

.files, .url, .submission {
    margin: 1rem 0;
}

.tags {
    justify-content: flex-end!important;
}
</style>
