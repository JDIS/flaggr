<template>
  <div id="signoutButton">
    <b-navbar-item tag="div">
      <b-button
        @click="disconnectUser()"
        type="is-danger"
      >{{ $t("nav.signout") }}</b-button>
    </b-navbar-item>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import store from '../store'

/**
 * Button to disconnect the connected user. Should only be displayed if the user is connected.
 */
export default Vue.extend({
  name: 'SignoutButton',
  data() {
    return {
    }
  },
  methods: {
    disconnectUser() {
      store.dispatch('user/disconnectUser')
    }
  },
  components: {
  }
});
</script>

<style scoped lang="scss">
@import "../style/theme.scss";

#signoutButton {
  position: relative;
  display: flex;
}
</style>
