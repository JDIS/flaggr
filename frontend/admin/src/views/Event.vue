<template>
  <div>
    <base-title :text="$t('event')" :color="color" />
    <base-subtitle :text="$t('event.general')" />
    <b-field :label="$t('event.name')">
      <b-input></b-input>
    </b-field>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseTitle from '../components/BaseTitle.vue';
import BaseSubtitle from '../components/BaseSubtitle.vue';

/**
 * Event administration page (choose event name, status, administrators, etc.)
 */
export default Vue.extend({
  name: 'event',
  data() {
    return {
      color: 'first'
    };
  },
  components: {
    BaseTitle,
    BaseSubtitle
  }
});
</script>

<style lang="scss">
</style>
