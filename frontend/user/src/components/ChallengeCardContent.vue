<template>
  <div class="columns">
    <div class="column is-three-quarters">
      <div class="solves-and-submissions columns">
        <div class="solves column is-paddingless" @click="toggleSolvesDetail()">
          {{$t('challenge.solves', { number: challenge.solves.length })}}
          <b-icon class="solvesToggle" :icon="displaySolvesDetails ? 'chevron-up' : 'chevron-down'" size="is-small" type="is-black"></b-icon>
        </div>
      </div>
      <b-collapse :open="displaySolvesDetails">
        <div v-for="solve in challenge.solves">
          <span class="is-size-7">{{ solve.team.name }}</span>
        </div>
        <br>
      </b-collapse>
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
      <div class="submission columns is-vcentered" v-if="!challenge.is_solved || isCorrect">
        <b-field :type="getInputType()" :message="getInputMessage()" class="column is-paddingless is-marginless">
          <b-input placeholder="FLAG-ThisIsAnExampl3" v-model="flag" expanded :disabled="isCorrect"></b-input>
          <p class="control">
            <b-button
              class="button is-primary"
              @click="submit"
              :loading="isLoading"
              :disabled="flag === '' || isCorrect"
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
import Vue from 'vue'
import { Challenge } from '@/models/challenge'
import { submitFlag } from '@/services/challenge.service'
import { sendAlertWithVariables } from '@/helpers'
import { TeamMixin } from '@/mixins/TeamMixin'

/**
 * Content of the challenge card
 */
export default Vue.extend({
  name: 'ChallengeCardContent',
  mixins: [TeamMixin],
  props: {
    challenge: Challenge
  },
  data() {
    return {
      flag: '',
      isLoading: false,
      isCorrect: false, // A correct flag was submitted
      isWrong: false, // A wrong flag was submitted,
      displaySolvesDetails: false,
    };
  },
  methods: {
    async submit() {
      this.resetValidationVariables();
      try {
        const res = await submitFlag(this.challenge.id, this.flag);
        this.setValidationVariables(res, this.flag);
      } catch (e) {
        sendAlertWithVariables('challenge.submissionError', {error: e.data.message})
        this.setValidationVariables(false, this.flag);
      }
    },
    resetValidationVariables() {
      this.isLoading = true;
      this.isCorrect = false;
      this.isWrong = false;
    },
    setValidationVariables(res: boolean, flag: string) {
      this.isLoading = false;
      if (res) {
        this.isCorrect = true;
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
    },
    toggleSolvesDetail() {
      if (this.challenge.solves.length > 0) {
        this.displaySolvesDetails = !this.displaySolvesDetails
      }
    },
  },
  components: {}
});
</script>

<style lang="scss">
@import "../plugins/buefy-theme.scss";

.solves {
    margin-bottom: 0.5rem;
    color: $light-3;
    cursor: pointer;
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

.history {
  margin-right: 0.3rem;
  cursor: pointer;
}

.old-submission {
  color: $danger !important;

  .correct {
    color: $success !important;
  }
}
</style>
