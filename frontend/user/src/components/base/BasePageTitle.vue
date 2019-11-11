<template>
    <h1 id="title" class="title">{{text}}</h1>
</template>

<script lang="ts">
import Vue from 'vue'

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

#title {
    margin-bottom: 0 !important;
    padding: 2rem 0;
}
</style>
