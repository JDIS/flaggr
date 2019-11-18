<template>
  <div id="signoutButton">
    <b-navbar-item tag="div">
      <b-button
        @click="disconnectParticipant()"
        type="is-danger"
      >{{ $t("nav.signout") }}</b-button>
    </b-navbar-item>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import store from '../store'

/**
 * Button to disconnect the connected participant. Should only be displayed if the participant is connected.
 */
export default Vue.extend({
  name: 'SignoutButton',
  data() {
    return {
    }
  },
  methods: {
    disconnectParticipant() {
      store.dispatch('participant/disconnectParticipant')
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
