<template>
  <div class="home">
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App" />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import HelloWorld from '../components/HelloWorld.vue';

/**
 * Homepage
 */
export default Vue.extend({
  name: 'home',
  components: {
    HelloWorld,
  },
});
</script>
