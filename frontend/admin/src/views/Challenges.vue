<template>
  <div>
    <base-title :text="$t('challenges')" :color="color" />
    <b-table
      :data="challenges"
      :columns="columns"
      striped
      hoverable
      checkable
      :checked-rows.sync="selectedChallenges"
      paginated
      per-page="10"
    ></b-table>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseTitle from '../components/BaseTitle.vue';
import BaseSubtitle from '../components/BaseSubtitle.vue';
import {Challenge} from '@/models/challenge';
import {getChallenges} from '@/services/challenge.service';

/**
 * Challenges administration page
 */
export default Vue.extend({
  name: 'challenges',
  data() {
    return {
      color: 'second',
      challenges: [] as Challenge[],
      selectedChallenges: [] as Challenge[],
      columns: [
        {
          field: 'id',
          label: this.$t('id'),
          width: '40',
          numeric: true,
          sortable: true
        },
        {
          field: 'name',
          label: this.$t('name'),
          sortable: true
        }
      ]
    };
  },
  async created() {
    this.challenges = await getChallenges();
  },
  components: {
    BaseTitle,
    BaseSubtitle
  }
});
</script>

<style lang="scss">
</style>
