<template>
  <div class="title-container">
    <div class="title colored-border" :class="`is-${color}`">
      {{ text }}
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

/**
 * Page title
 */
export default Vue.extend({
  name: 'BaseTitle',
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
.title {
  text-transform: uppercase;
  font-weight: 700;
  border-bottom-width: 0.35rem;
  border-bottom-style: solid;
}
</style>
