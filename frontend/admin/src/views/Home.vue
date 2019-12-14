<template>
  <div id="home">
    <LoginModal v-if="!isConnected()"></LoginModal>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import LoginModal from '@/components/LoginModal.vue';
import {AdminMixin} from '@/mixins/AdminMixin';

/**
 * Home page
 */
export default Vue.extend({
  name: 'home',
  mixins: [AdminMixin],
  components: {
    LoginModal
  }
});
</script>
