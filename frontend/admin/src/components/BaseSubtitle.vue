<template>
  <div class="subtitle-container">
    <div class="subtitle">{{ text }}</div>
  </div>
</template>

<script lang="ts">
    import Vue from "vue";

    /**
 * Subtitle for page section
 */
export default Vue.extend({
  name: 'BaseSubtitle',
  props: {
    text: String
  },
  data() {
    return {};
  }
});
</script>

<style lang="scss">
.subtitle-container {
  margin-top: 2rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid #f4f4f4;
}

.subtitle {
  font-size: 1.5rem;
}
</style>
