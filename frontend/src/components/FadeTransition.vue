<template>
  <transition name="fade">
    <slot></slot>
  </transition>
</template>

<script lang="ts">
import Vue from 'vue'

/**
 * Component that fades in and out its content (see ConnectionButtonContainer for an example usage)
 */
export default Vue.extend({
  name: 'FadeTransition',
  data() {
    return {}
  },
  methods: {},
  components: {}
})
</script>

<style scoped lang="scss">
</style>
