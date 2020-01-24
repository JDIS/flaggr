<template>
  <div class="page-content">
    <base-title :text="$t('participants')" :color="color" />

    <b-table
            :data="participants"
            striped
            hoverable
            paginated
            per-page="10"
    >
      <template slot-scope="props">
        <b-table-column field="id" :label="$t('id')" sortable>
          {{ props.row.id }}
        </b-table-column>
        <b-table-column field="username" :label="$t('username')" sortable>
          {{ props.row.user.username }}
        </b-table-column>
        <b-table-column field="email" :label="$t('email')" sortable>
          {{ props.row.user.email }}
        </b-table-column>
      </template>
    </b-table>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseTitle from '../components/BaseTitle.vue';
import BaseSubtitle from '../components/BaseSubtitle.vue';
import {sendErrorAlert} from '@/helpers/alerts.helper'
import {getParticipants} from '@/services/participants.service'
import {Participant} from '@/models/participant.js'

/**
 * Participants administration page
 */
export default Vue.extend({
  name: 'participants',
  data() {
    return {
      color: 'third',
      participants: [] as Participant[],
    };
  },
  async created() {
    try {
      this.participants = await getParticipants(this.$route.params.eventId);
    } catch (error) {
      sendErrorAlert('participants.get.error', error);
    }
  },
  components: {
    BaseTitle,
    BaseSubtitle
  }
});
</script>

<style lang="scss">
</style>
