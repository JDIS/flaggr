<!-- Connection button and modal for signin/signup -->

<template>
  <div id="connectionButtonContainer">
    <b-navbar-item tag="div">
      <b-button @click="toggleConnectionModalVisibility()" type="is-primary" >{{$t('nav.connectionInscription')}}</b-button>
    </b-navbar-item>
    <CustomModal v-if="connectionModalShown" :visible="connectionModalShown" v-on:close="toggleConnectionModalVisibility()">
      <ConnectionModal class="connectionModalComponent"></ConnectionModal>
    </CustomModal>
  </div>
</template>

<script lang="ts">
    import Vue from 'vue';
    import ConnectionModal from '@/components/ConnectionModal.vue';
    import CustomModal from '@/components/CustomModal.vue';

    export default Vue.extend({
  name: 'ConnectionButtonContainer',
  data() {
    return {
      connectionModalShown: false,
      isConnected: true, // To change later
    }
  },
  methods: {
      toggleConnectionModalVisibility() {
          this.connectionModalShown = !this.connectionModalShown
      }
  },
  components: {
    ConnectionModal,
    CustomModal,
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
