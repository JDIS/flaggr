<template>
  <div id="app">
    <app-header />
    <div class="columns">
      <div class="column is-3 sidebar">
        <app-navigation />
      </div>
      <div class="column is-9 content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import AppHeader from './components/AppHeader.vue';
import AppNavigation from './components/AppNavigation.vue';

export default Vue.extend({
  name: 'app',
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
  background-color: $grey-light;
}

.content {
  overflow: auto;
  padding: 0;
  box-shadow: inset 0px 0px 5px 0px $grey-light;
}
</style>
