<template>
  <div id="app">
    <navigation-bar />
    <router-view />
    <AppFooter></AppFooter>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import {NavigationBar} from './components';
import AppFooter from '@/components/AppFooter.vue';

export default Vue.extend({
  name: 'app',
  components: {
    NavigationBar,
    AppFooter
  }
});
</script>


<style lang="scss">
@import 'style/fonts.scss';
@import 'plugins/buefy-theme.scss';
</style>
