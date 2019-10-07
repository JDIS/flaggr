<template>
    <h1 class="title">{{text}}</h1>
</template>

<script lang="ts">
import Vue from 'vue';

/**
 * Base title for the top of a page
 */
export default Vue.extend({
  name: 'BasePageTitle',
  props: {
    text: String,
  }
});
</script>

<style lang="scss">
.title {
    padding: 2rem 0;
}
</style>
