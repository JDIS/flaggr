<template>
  <div>
    <base-subtitle :text="$t('event.theme')" />
    <b-field :label="`${$t('event.logo')} :`">
      <single-file-upload :color="color" @input="updateLogo" />
    </b-field>
    <b-field :label="`${$t('event.customcss')} :`">
      <b-input type="textarea" v-model="config.customCSS" @input="onInput"></b-input>
    </b-field>
    <b-field>
      <template slot="label">
        {{`${$t('event.homepage')} :`}}
        <b-tooltip :label="$t('event.homepage.tooltip')" position="is-right">
          <b-icon icon="help-circle"></b-icon>
        </b-tooltip>
      </template>
      <b-input type="textarea"></b-input>
    </b-field>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BaseSubtitle from './BaseSubtitle.vue';
import SingleFileUpload from './SingleFileUpload.vue';
import { EventTheme } from '../models/eventTheme';

/**
 * Configuration of event theme
 */
export default Vue.extend({
  name: 'EventThemeConfig',
  props: {
    config: Object as () => EventTheme,
    color: String
  },
  data() {
    return {};
  },
  methods: {
    onInput() {
      this.$emit('input', this.config);
    },
    updateLogo(file: File) {
      this.config.logo = file;
    }
  },
  components: {
    BaseSubtitle,
    SingleFileUpload
  }
});
</script>

<style lang="scss" scoped>
.b-tooltip {
  margin-left: 1rem;
}
</style>
