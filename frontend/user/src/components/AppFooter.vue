<!-- footer component, always present -->
<template>
  <footer class="footer">
    <div class="content has-text-centered">
      <div class="is-size-7">{{ $t('projectName') }} - 2019-2019 - Source</div>
    </div>
  </footer>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'AppFooter',
});
</script>

<style scoped lang="scss">

.footer {
  margin-top: 0.5rem;
  width: 100vw;
  position: absolute;
  bottom: 0;
}

</style>
