<template>
  <div class="is-full-height">
    <div class="page-content">
      <base-title :text="$t('event')" :color="color" />
      <div class="form">
        <event-general-config :config="event" @input="updateGeneralConfig" />
        <event-theme-config v-if="false" :color="color" :config="event" @input="updateTheme" /> <!-- Unsupported for now -->
      </div>
    </div>
    <bottom-bar>
      <b-button :class="`is-${color}`" @click="save">{{ $t('save') }}</b-button>
      <router-link to="/event">
        <b-button class="is-light">{{ $t('cancel') }}</b-button>
      </router-link>
    </bottom-bar>
    <div class="page-content" v-if="false"> <!-- Unsupported for now -->
      <base-subtitle :text="$t('event.admins')" />
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseTitle from '../components/BaseTitle.vue';
import BaseSubtitle from '../components/BaseSubtitle.vue';
import BottomBar from '../components/BottomBar.vue';
import EventGeneralConfig from '../components/EventGeneralConfig.vue';
import EventThemeConfig from '../components/EventThemeConfig.vue';
import {Event} from '../models/event';
import {GeneralEvent} from '../models/generalEvent';
import {EventTheme} from '../models/eventTheme';
import {editEvent, getEvent, getEvents} from '@/services/event.service';
import {sendAlert, sendErrorAlert} from '@/helpers/alerts.helper';
import store from '@/store';

/**
 * Event administration page (choose event name, status, administrators, etc.)
 */
export default Vue.extend({
  name: 'event',
  data() {
    return {
      color: 'first',
      event: new Event()
    };
  },
  created() {
    getEvent(this.$route.params.eventId)
        .then((event) => this.event = event)
        .catch((error) => sendErrorAlert('event.get.error', error))
  },
  methods: {
    save() {
      editEvent(this.event, this.$route.params.eventId)
          .then((event) => {
            sendAlert('event.updated', {type: 'is-success'})
            getEvents().then((events) => {
              store.dispatch('event/setEvents', events)
              const currentEvent = events.find((event2) => event2.id === parseInt(this.$route.params.eventId, 0.4))
              store.dispatch('event/setEvent', currentEvent)
            })
          })
          .catch((error) => sendErrorAlert('event.update.error', error))
    },
    updateGeneralConfig(config: GeneralEvent) {
      this.event.name = config.name;
      this.event.url = config.url;
      this.event.flagFormat = config.flagFormat;
      this.event.teamSize = config.teamSize;
      this.event.is_visible = config.is_visible;
      this.event.is_visible = config.is_open;
    },
    updateTheme(theme: EventTheme) {
      this.event.customCSS = theme.customCSS;
      this.event.front_page = theme.front_page;
      this.event.logo = theme.logo;
    }
  },
  components: {
    BaseTitle,
    BaseSubtitle,
    BottomBar,
    EventGeneralConfig,
    EventThemeConfig
  }
});
</script>

<style lang="scss" scoped>
</style>
