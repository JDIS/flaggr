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
        <a v-for="link in challenge.links" v-bind:key="link" :href="link" target="_blank">
          <b-icon icon="open-in-new" size="is-small"></b-icon>
          {{link}}
        </a>
      </div>
      <div class="submission" v-if="!challenge.isSolved || isCorrect">
        <b-field :type="getInputType()" :message="getInputMessage()">
          <b-input placeholder="FLAG-ThisIsAnExampl3" v-model="flag" expanded :disabled="isCorrect"></b-input>
          <p class="control">
            <b-button
              class="button is-primary"
              @click="submit"
              :loading="isLoading"
              :disabled="isCorrect"
            >{{$t('submit')}}</b-button>
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
import { submitFlag } from '../services/challenge.service';

/**
 * Content of the challenge card
 */
export default Vue.extend({
  name: 'ChallengeCardContent',
  props: {
    challenge: Challenge
  },
  data() {
    return {
      flag: '',
      isLoading: false,
      isCorrect: false, // A correct flag was submitted
      isWrong: false // A wrong flag was submitted
    };
  },
  methods: {
    async submit() {
      this.resetValidationVariables();
      const res = await submitFlag(this.challenge.id, this.flag);
      this.setValidationVariables(res);
    },
    resetValidationVariables() {
      this.isLoading = true;
      this.isCorrect = false;
      this.isWrong = false;
    },
    setValidationVariables(res: boolean) {
      this.isLoading = false;
      if (res) {
        this.isCorrect = true;
        this.challenge.isSolved = true;
        this.$emit('solved');
      } else {
        this.isWrong = true;
      }
    },
    getInputType() {
      if (this.isWrong) {
        return 'is-danger';
      } else if (this.isCorrect) {
        return 'is-success';
      } else {
        return '';
      }
    },
    getInputMessage() {
      if (this.isWrong) {
        return this.$t('challenge.isWrong');
      } else if (this.isCorrect) {
        return this.$t('challenge.isCorrect');
      } else {
        return '';
      }
    }
  },
  components: {}
});
</script>

<style lang="scss">
@import "../style/theme.scss";

.solves {
    margin-bottom: 0.5rem;
    color: $light-3;
}
.description {
    font-weight: 300;
}

.files, .url, .submission {
    margin: 1rem 0;

    .mdi-light:before {
      color: inherit;
    }
}

.tags {
    justify-content: flex-end!important;
    margin-right: 0!important;
    margin-left: 0.5rem!important;
}

.submission {
  .button[disabled], .input[disabled] {
    cursor: default;
  }
} 

.field {
  flex-wrap: wrap;
}

.help {
  flex-basis: 100%;
}
</style>
