<template>
  <div class="bottom-bar">
    <slot></slot>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

/**
 * Sticky bar at the bottom of a page
 */
export default Vue.extend({
  name: 'BottomBar',
  props: {
    text: String,
    color: String
  },
  data() {
    return {};
  }
});
</script>

<style lang="scss">
@import '../style/theme.scss';

.bottom-bar {
  position: sticky;
  width: 100%;
  bottom: 0;
  background: $grey-light;
  padding: 0.75rem 3rem;

  button {
    margin-right: 1rem;
  }
}
</style>
