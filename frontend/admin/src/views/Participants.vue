<template>
  <div>
    <base-title :text="$t('participants')" :color="color" />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseTitle from '../components/BaseTitle.vue';
import BaseSubtitle from '../components/BaseSubtitle.vue';

/**
 * Participants administration page
 */
export default Vue.extend({
  name: 'participants',
  data() {
    return {
      color: 'third'
    };
  },
  components: {
    BaseTitle,
    BaseSubtitle
  }
});
</script>

<style lang="scss">
</style>