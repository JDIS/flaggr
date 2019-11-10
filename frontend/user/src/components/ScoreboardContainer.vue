<template>
  <div id="scoreboard-container">
    <b-table
      :data="data"
      :columns="columns"
      :default-sort="['position', 'asc']"
      sortable
      icon-pack="mdi-light"
    ></b-table>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { Challenge } from '../models/challenge';
import ChallengeCardHeader from './ChallengeCardHeader.vue';
import ChallengeCardContent from './ChallengeCardContent.vue';

/**
 * Component to display the scoreboard (holds both the graph and the table)
 */
export default Vue.extend({
  name: 'ScoreboardContainer',
  data() {
    return {
      data: [
        // TODO Plug this with backend
        {
          position: 2,
          team_name: 'Jesse',
          affiliation: 'Sciences',
          date: '2016-10-15 13:43:27',
          score: 6800
        },
        {
          position: 1,
          team_name: 'John',
          affiliation: 'Génie',
          date: '2016-12-15 06:00:53',
          score: 42000
        },
        {
          position: 3,
          team_name: 'Tina',
          affiliation: 'Génie',
          date: '2016-04-26 06:26:28',
          score: 420
        },
        {
          position: 4,
          team_name: 'Clarence',
          affiliation: 'Sciences',
          date: '2016-04-10 10:28:46',
          score: 70
        },
        {
          position: 5,
          team_name: 'Anne',
          affiliation: 'Sciences',
          date: '2016-12-06 14:38:38',
          score: 4.2
        }
      ],
      columns: [
        {
          field: 'position',
          label: this.$t('scoreboard.rank'),
          width: '40',
          numeric: true,
          sortable: true
        },
        {
          field: 'team_name',
          label: this.$t('scoreboard.team'),
          sortable: true
        },
        {
          field: 'affiliation',
          label: this.$t('scoreboard.affiliation'),
          sortable: true
        },
        {
          field: 'date',
          label: this.$t('scoreboard.lastUpdate'),
          sortable: true
        },
        {
          field: 'score',
          label: this.$t('scoreboard.score'),
          sortable: true
        }
      ]
    };
  },
  props: {
    challenge: Challenge
  },
  components: {
    ChallengeCardHeader,
    ChallengeCardContent
  }
});
</script>

<style lang="scss">
@import "../style/theme.scss";
@import "../plugins/buefy-theme.scss";

#scoreboard-container {
  margin-bottom: 2rem;
}


.table {
  background: none;
  color: $white-bis;
  &tr:nth-child(even) {
    background: $grey;
  }

  th {
    .th-wrap {
      color: $primary-invert;
    }
    &.is-sortable {
      border-color: $grey-light;
    }
    &.is-current-sort, &.is-sortable:hover {
      border-color: $grey-lighter!important;
    }
  }
}
</style>
