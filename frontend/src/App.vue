<template>
  <div id="app">
    <navigation-bar />
    <router-view />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { NavigationBar } from './components';

export default Vue.extend({
  name: 'app',
  components: {
    NavigationBar
  }
});
</script>

<style lang="scss">
@import '@/style/fonts.scss';
@import '@/plugins/buefy-theme.scss';
</style>
