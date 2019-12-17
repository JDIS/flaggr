<template>
  <div id="app">
    <navigation-bar v-show="$router.currentRoute.meta.showNavbar" />
    <router-view />
    <AppFooter></AppFooter>
    <div class="footer-margin"></div>
    <div id="request-status"
         :class="{'requestInProgress': $store.state.network.requestsInProgress.length > 0,
                  'hasError': $store.state.network.hasError === true}"></div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import NavigationBar from './components/NavigationBar.vue'
import AppFooter from './components/AppFooter.vue'

export default Vue.extend({
  name: 'app',
  components: {
    NavigationBar,
    AppFooter
  },
  created() {
    /**
     * Fetch the event every 10 seconds to check for updates
     */
    window.setInterval(() => {
      if (this.$route.params.eventId) {
        this.$store.dispatch('event/fetchEvent', this.$route.params.eventId)
      }
    }, 10000)
  }
});
</script>


<style lang="scss">
@import 'plugins/buefy-theme.scss';

#app {
  position: relative;
  display: flow-root;
  min-height: 100vh;

  .footer-margin {
    margin-top: 3rem;
  }
}

#request-status {
  position: fixed;
  bottom:0;
  width:100%;
  height:2px;

  &.requestInProgress {
    background: yellow;
  }

  &.hasError {
    background: red;
  }
}
</style>
