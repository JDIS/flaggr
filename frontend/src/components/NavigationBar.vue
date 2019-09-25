<template>
  <b-navbar class="has-shadow">
    <template slot="brand">
      <b-navbar-item tag="router-link" :to="{ path: '/' }">
        <img src="@/assets/jdis_logo.svg" />
        <h1 class="title">JDIS</h1>
      </b-navbar-item>
    </template>
    <template slot="start">
      <navigation-bar-links />
    </template>

    <template slot="end">
      <b-navbar-item tag="div">
          <base-button text="Connexion / Inscription" />
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<script lang="ts">
import Vue from 'vue';
import { BaseButton, NavigationBarLinks } from '../components';

export default Vue.extend({
  name: 'NavigationBar',
  components: {
    BaseButton,
    NavigationBarLinks
  }
});
</script>

<style scoped lang="scss">
.navbar-item img {
  margin-left: 1rem;
}
.title {
  font-size: 1.5rem;
  padding: 0.5rem;
}
</style>
