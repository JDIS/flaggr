<template>
  <div class="event-selection">
    <h1>{{ $t('eventSelection.chooseEvent') }}</h1>
    <div v-for="event in events">
      <router-link :to="{ name: 'home', params: { eventId: event.id }}" class="event">{{ event.name }}</router-link>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { EventMixin } from '@/mixins/EventMixin'
import { getAllEvents } from '@/services/event.service'
import { Event } from '@/models/event'

/**
 * View to select an event in the list of events the platform has. Serves as the root page.
 */
export default Vue.extend({
  name: 'EventSelection',
  mixins: [EventMixin],
  data() {
    return {
      events: [] as Event[]
    }
  },
  mounted() {
    getAllEvents().then((events) => {
      this.events = events
    })
  },
  components: {
  },
});
</script>

<style scoped lang="scss">
@import "../plugins/buefy-theme";

h1 {
  font-size: 140%;
  margin-bottom: 1rem;
}

.event-selection {
  max-width: 500px;
  margin: auto;
  margin-top: 3rem;
  padding: 1rem;
  text-align: center;
  background: $dark-3;
  border-radius: 0.4rem;
  box-shadow: 0 0 0.2rem black;

  .event {
    color: $light-0;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
