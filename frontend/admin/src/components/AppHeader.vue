<template>
  <b-navbar shadow type="is-dark" fixed-top>
    <template slot="brand">
      <b-navbar-item tag="div">
        <h1>JDIS</h1>
      </b-navbar-item>
    </template>
    <template slot="start">
      <b-navbar-dropdown label="Qualifications CS Games 2020">
        <b-navbar-item href="#">JDIS Games 2020</b-navbar-item>
        <b-navbar-item href="#">
          <b-icon icon="plus-circle" size="is-small"></b-icon>
          <strong>{{ this.$t('event.new') }}</strong>
        </b-navbar-item>
      </b-navbar-dropdown>
    </template>

    <template slot="end">
      <b-navbar-item tag="div">
        <b-button type="is-primary">{{ this.$t('logout') }}</b-button>
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'AppHeader',
  data() {
    return {};
  },
  methods: {},
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
