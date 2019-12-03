<template>
  <div id="scoreboard-container">
    <b-button icon-right="reload" type="is-primary" size="is-small"
              @click="fetchScoreboard()" class="is-pulled-right"
              :disabled="isFetchingScoreboard"
    ></b-button>
    <div class="is-clearfix"></div>
    <b-switch v-model="automaticReload" type="is-success"
              class="is-pulled-right">
      {{ $t('scoreboard.autoreload') }}
    </b-switch>
    <b-table :loading="isFetchingScoreboard"
      :data="data"
      :columns="columns"
      :default-sort="['position', 'asc']"
      sortable
      icon-pack="mdi-light"
    ></b-table>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { getScoreboard } from '@/services/scoreboard.service'
import { ScoreboardEntry } from '@/models/scoreboard'
import { FlaskRebarError } from '@/models/flask_rebar_error'
import { sendAlertWithVariables } from '@/helpers'
import { EventMixin } from '@/mixins/EventMixin'

/**
 * Component to display the scoreboard (holds both the graph and the table)
 */
export default Vue.extend({
  name: 'ScoreboardContainer',
  mixins: [EventMixin],
  data() {
    return {
      isFetchingScoreboard: false,
      automaticReload: false,
      data: [] as ScoreboardEntry[],
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
          sortable: true,
        },
        {
          field: 'solved_challenges',
          label: this.$t('scoreboard.solvedChallenges'),
          sortable: true,
          width: '170',

        },
        {
          field: 'last_submission',
          label: this.$t('scoreboard.lastUpdate'),
          sortable: true
        },
        {
          field: 'points',
          label: this.$t('scoreboard.score'),
          sortable: true
        }
      ]
    };
  },
  created() {
    // @ts-ignore
    if (this.isSoloEvent) {
      this.columns.find((col) => col.field === 'team_name')!.label = this.$t('scoreboard.participant')
    }
  },
  mounted() {
    // @ts-ignore
    if (this.isSoloEvent) {
      this.columns.find((col) => col.field === 'team_name')!.label = this.$t('scoreboard.participant')
    }
    window.setInterval(() => {
      if (this.automaticReload && this.$router.currentRoute.name === 'scoreboard') {
        this.fetchScoreboard()
      }
    }, 10000)
    this.fetchScoreboard()

  },
  methods: {
    /**
     * Fetch scoreboard and update models, or display error on failure.
     */
    fetchScoreboard() {
      this.isFetchingScoreboard = true
      getScoreboard().then((scoreboardEntries) => {
        this.data = scoreboardEntries
        this.isFetchingScoreboard = false
      }).catch((error: FlaskRebarError) => {
        sendAlertWithVariables('scoreboard.errorWhileFetching', {error: error.message})
        this.isFetchingScoreboard = false
      })
    }
  },
  computed: {},
  props: {
  },
  components: {
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
