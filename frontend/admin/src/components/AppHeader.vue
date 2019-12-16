<template>
  <b-navbar shadow type="is-dark" fixed-top>
    <template slot="brand">
      <b-navbar-item tag="div">
        <h1>{{ $t('projectName') }}</h1>
      </b-navbar-item>
    </template>
    <template slot="start">
      <b-navbar-dropdown :label="event ? event.name : $t('pickEvent')" v-if="isConnected()">
        <router-link v-for="event in events" :to="`/${event.id}`">
          <b-navbar-item>{{ event.name }}</b-navbar-item>
        </router-link>
        <b-navbar-item @click="createEvent()">
          <b-icon icon="plus-circle" size="is-small"></b-icon>
          <strong>{{ this.$t('event.new') }}</strong>
        </b-navbar-item>
      </b-navbar-dropdown>
    </template>

    <template slot="end">
      <b-navbar-item tag="div" v-if="isConnected()">
        <b-button type="is-primary" @click="logout()">{{ this.$t('logout') }}</b-button>
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<script lang="ts">
import Vue from 'vue';
import {AdminMixin} from '@/mixins/AdminMixin';
import {EventMixin} from '@/mixins/EventMixin';
import {createEvent, getEvents} from '@/services/event.service';
import {sendErrorAlert} from '@/helpers/alerts.helper';
import store from '@/store';

/**
 * Application header (at the top of the page)
 */
export default Vue.extend({
  name: 'AppHeader',
  mixins: [AdminMixin, EventMixin],
  data() {
    return {
    };
  },
  methods: {
    logout() {
      this.$store.dispatch('admin/disconnectAdmin')
    },

    /**
     * Create an event and then redirects to the created event page.
     * Sets the events and event state accordingly.
     */
    createEvent() {
      createEvent()
          .then((event) => {
            getEvents().then((events) => {
              store.dispatch('event/setEvents', events)
              const currentEvent = events.find((event2) => event2.id === event.id)
              store.dispatch('event/setEvent', currentEvent)
              this.$router.push({name: 'event', params: {eventId: event.id}})
            })
          })
          .catch((error) => sendErrorAlert('createEvent.error', error))
    }
  },
  components: {}
});
</script>

<style lang="scss">
@import '../plugins/buefy-theme.scss';
.navbar {
  align-items: center;

  h1 {
    margin-left: 1rem;
    font-size: 1.5rem;
    font-weight: 600;
  }
  .navbar-start {
    margin-left: 1rem;
    font-family: $family-secondary;
    font-size: 0.95rem;

    .icon {
      margin-right: 0.5rem;
    }
  }
}
</style>
