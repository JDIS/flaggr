<template>
  <div class="is-full-height">
    <div class="page-content">
      <base-title :text="$t('event')" :color="color" />
      <div class="form">
        <event-general-config :config="event" @input="updateGeneralConfig" />
        <event-theme-config :color="color" :config="event" @input="updateTheme" />
      </div>
    </div>
    <bottom-bar>
      <b-button :class="`is-${color}`" @click="save">{{ $t('save') }}</b-button>
      <router-link to="/event">
        <b-button class="is-light">{{ $t('cancel') }}</b-button>
      </router-link>
    </bottom-bar>
    <div class="page-content">
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
import { Event } from '../models/event';
import { GeneralEvent } from '../models/generalEvent';
import { EventTheme } from '../models/eventTheme';

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
  methods: {
    save(): boolean {
      console.log('save');
      return true;
    },
    updateGeneralConfig(config: GeneralEvent) {
      this.event.name = config.name;
      this.event.url = config.url;
      this.event.flagFormat = config.flagFormat;
      this.event.teamSize = config.teamSize;
      this.event.visible = config.visible;
      this.event.open = config.open;
    },
    updateTheme(theme: EventTheme) {
      this.event.customCSS = theme.customCSS;
      this.event.homePage = theme.homePage;
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
