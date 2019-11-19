<template>
  <div>
    <base-title :text="$t('challenges')" :color="color" />
    <b-table
      :data="challenges"
      striped
      hoverable
      checkable
      :checked-rows.sync="selectedChallenges"
      paginated
      per-page="10"
      :loading="isLoading"
    >
      <template slot-scope="props">
        <b-table-column field="name" :label="$t('name')" sortable>{{ props.row.name }}</b-table-column>
        <b-table-column field="track" :label="$t('track')" sortable>{{ props.row.track.name }}</b-table-column>
        <b-table-column field="points" :label="$t('points')" numeric sortable>{{ props.row.points }}</b-table-column>

        <b-table-column field="visible" :label="$t('visible')" centered sortable>
          <span>
            <b-icon
              :icon="props.row.visible ? 'eye' : 'eye-off'"
              class="clickable-icon"
              :class="{ 'not-visible': !props.row.visible }"
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
        <b-button :class="`is-${color}`" icon-left="plus">{{ $t('new') }}</b-button>
      </template>
    </b-table>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseTitle from '../components/BaseTitle.vue';
import BaseSubtitle from '../components/BaseSubtitle.vue';
import { Challenge } from '../models/challenge';
import { getChallenges, getChallengeById } from '../services/challenge.service';

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
    this.challenges = await getChallenges();
    this.isLoading = false;
  },
  methods: {
    deleteChallenge(challenge: Challenge) {
      console.log(`delete ${challenge.name}`);
      // TODO : api call
    },
    toggleVisibility(challenge: Challenge) {
      console.log(`update visibility ${challenge.name}`);
      challenge.visible = !challenge.visible;
      // TODO : api call
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