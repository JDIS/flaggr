<!-- Connection button and modal for signin/signup -->

<template>
  <div id="connectionButtonContainer">
    <b-navbar-item tag="div">
      <b-button
        @click="toggleVisibility()"
        type="is-primary"
      >{{ $t("nav.connectionInscription") }}</b-button>
    </b-navbar-item>
    <FadeTransition>
      <CustomModal v-if="shown" :visible="shown" v-on:close="toggleVisibility()">
        <ConnectionModal class="connectionModalComponent"></ConnectionModal>
      </CustomModal>
    </FadeTransition>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import ConnectionModal from '@/components/ConnectionModal.vue'
import CustomModal from '@/components/CustomModal.vue'
import FadeTransition from '@/components/FadeTransition.vue'

export default Vue.extend({
  name: 'ConnectionButtonContainer',
  data() {
    return {
      shown: false,
      isConnected: true, // To change later
    }
  },
  methods: {
    toggleVisibility() {
      this.shown = !this.shown
    }
  },
  components: {
    ConnectionModal,
    CustomModal,
    FadeTransition
  }
});
</script>

<style scoped lang="scss">
@import "../style/theme.scss";

#connectionButtonContainer {
  position: relative;
  display: flex;
}
</style>
