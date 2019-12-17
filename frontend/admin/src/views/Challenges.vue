<template>
  <div class="page-content">
    <base-title :text="$t('challenges')" :color="color" />
    <b-table
      :data="challenges"
      striped
      hoverable
      :checked-rows.sync="selectedChallenges"
      paginated
      per-page="10"
      :loading="isLoading"
    >
      <template slot-scope="props">
        <b-table-column field="name" :label="$t('name')" sortable>
          <router-link
            :to="{ name: 'edit-challenge', params: {id: props.row.id } }"
          >{{ props.row.name }}</router-link>
        </b-table-column>
        <b-table-column field="track" :label="$t('track')" sortable>
          <span v-if="props.row.category">{{ props.row.category }}</span>
        </b-table-column>
        <b-table-column field="points" :label="$t('points')" numeric sortable>{{ props.row.points }}</b-table-column>

        <b-table-column field="visible" :label="$t('visible')" centered sortable>
          <span>
            <b-icon
              :icon="!props.row.hidden ? 'eye' : 'eye-off'"
              class="clickable-icon"
              :class="{ 'not-visible': props.row.hidden }"
              @click.native="toggleVisibility(props.row)"
            ></b-icon>
          </span>
        </b-table-column>

        <b-table-column custom-key="delete">
          <b-icon
            icon="close"
            class="clickable-icon"
            type="is-danger"
            @click.native="deleteChallenge(props.row)"
          ></b-icon>
        </b-table-column>
      </template>

      <template slot="empty">
        <div class="section" v-if="!isLoading">
          <div class="content has-text-grey has-text-centered">
            <b-icon icon="flag-variant-outline" size="is-medium"></b-icon>
            <p>{{ $t('challenges.empty') }}</p>
          </div>
        </div>
      </template>

      <template slot="bottom-left">
        <router-link :to="{ name: 'new-challenge' }">
          <b-button :class="`is-${color}`" icon-left="plus">{{ $t('new') }}</b-button>
        </router-link>
      </template>
    </b-table>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseTitle from '../components/BaseTitle.vue';
import BaseSubtitle from '../components/BaseSubtitle.vue';
import {Challenge} from '@/models/challenge';
import {
  deleteChallenge,
  getChallenges,
  makeChallengeHidden,
  makeChallengeVisible,
  updateChallenge
} from '@/services/challenge.service';
import {sendAlert, sendAlertWithVariables, sendErrorAlert} from '@/helpers/alerts.helper';

/**
 * Challenges administration page
 */
export default Vue.extend({
  name: 'challenges',
  data() {
    return {
      color: 'second',
      isLoading: true,
      challenges: [] as Challenge[],
      selectedChallenges: [] as Challenge[]
    };
  },
  async created() {
    try {
      this.challenges = await getChallenges();
    } catch (error) {
      sendErrorAlert('challenges.get.error', error);
    } finally {
      this.isLoading = false;
    }
  },
  methods: {
    /**
     * Delete the challenge and display success or error on completion
     */
    async deleteChallenge(challenge: Challenge) {
      try {
        await deleteChallenge(challenge.id);
        this.challenges = this.challenges.filter((x) => x !== challenge);
        sendAlert('challenges.delete.success', { type: 'is-success'});
      } catch (error) {
        sendErrorAlert('challenges.delete.error', error);
      }
    },
    /**
     * Toggle the challenge visibility and display success or error on completion
     */
    async toggleVisibility(challenge: Challenge) {
      try {
        let text
        if (!challenge.hidden) {
          await makeChallengeHidden(challenge.id)
          text = 'challenges.hidden.success'
          challenge.hidden = true;

        } else {
          await makeChallengeVisible(challenge.id)
          text = 'challenges.visible.success'
          challenge.hidden = false;
        }
        sendAlertWithVariables(text, { name: challenge.name }, { type: 'is-success'});
      } catch (error) {
        sendErrorAlert('challenges.update.error', error);
      }
    }
  },
  components: {
    BaseTitle,
    BaseSubtitle
  }
});
</script>

<style lang="scss">
.b-table.is-loading:after {
  border-bottom-color: #000;
  border-left-color: #000;
}

.table-wrapper {
  margin-top: 1rem;
}

.clickable-icon {
  cursor: pointer;
  transition: 0.25s;

  &:hover {
    opacity: 0.5;
    transition: 0.25s;
  }
}

.clickable-icon.not-visible {
  opacity: 0.5;

  &:hover {
    opacity: 1;
  }
}
</style>
