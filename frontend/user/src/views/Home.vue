<template>
  <div class="home">
    <div class="container front-page">
      <vue-markdown v-if="event">{{ event.front_page }}</vue-markdown>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import HelloWorld from '../components/HelloWorld.vue'
import { EventMixin } from '@/mixins/EventMixin'
import VueMarkdown from 'vue-markdown'

/**
 * Homepage
 */
export default Vue.extend({
  name: 'home',
  mixins: [EventMixin],
  components: {
    HelloWorld,
    VueMarkdown
  },
});
</script>

<style scoped lang="scss">
.front-page {
  margin-top: 1rem;
  max-width: 1300px;
}
</style>
