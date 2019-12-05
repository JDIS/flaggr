<template>
  <div class="home">
    <div id="login-modal">
      <LoginModal></LoginModal>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import LoginModal from '@/components/LoginModal.vue';

/**
 * Login page
 */
export default Vue.extend({
  name: 'login',
  components: {
    LoginModal
  }
});
</script>

<style scoped lang="scss">
#login-modal {
  max-width: 400px;
  margin: auto;
  margin-top: 2rem;
}
</style>
