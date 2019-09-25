<template>
  <a class="button is-primary">{{text}}</a>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'BaseButton',
  props: {
    text: String,
  }
});
</script>

<style scoped lang="scss">
.button {
  font-weight: 600;
  font-size: 0.75rem;
  padding: 1rem;
  text-transform: uppercase;
}
</style>
