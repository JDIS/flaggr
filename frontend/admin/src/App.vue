<template>
  <div id="app">
    <app-header />
    <div class="columns">
      <div class="column is-one-fifth sidebar" v-if="isConnected() && event">
        <app-navigation />
      </div>
      <div class="column app-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import AppHeader from './components/AppHeader.vue';
import AppNavigation from './components/AppNavigation.vue';
import {AdminMixin} from '@/mixins/AdminMixin';
import {EventMixin} from './mixins/EventMixin';

export default Vue.extend({
  name: 'app',
  mixins: [AdminMixin, EventMixin],
  components: {
    AppHeader,
    AppNavigation
  }
});
</script>

<style lang="scss">
@import 'plugins/buefy-theme.scss';
html, body, #app, .columns {
  height: 100%;
  overflow: hidden;
}

.columns {
  margin: 0;
}

.sidebar {
  height: 100%;
  left: 0;
  padding: 0;
  background-color: $grey-lighter;
}

.app-content {
  overflow: auto;
  padding: 0;
  box-shadow: inset 0px 0px 5px 0px $grey-lighter;
}
</style>
