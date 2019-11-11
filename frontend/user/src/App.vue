<template>
  <div id="app">
    <navigation-bar />
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
import store from './store'

export default Vue.extend({
  name: 'app',
  mounted() {
    store.dispatch('user/fetchUser')
  },
  components: {
    NavigationBar,
    AppFooter
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
