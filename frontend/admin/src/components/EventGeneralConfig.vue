<template>
  <div>
    <b-field :label="`${$t('event.name')} :`">
      <b-input v-model="config.name" @input="onInput"></b-input>
    </b-field>
    <b-field :label="`${$t('event.url')} :`">
      <b-input v-model="config.url" @input="onInput"></b-input>
    </b-field>
    <b-field :label="`${$t('event.flagformat')} :`">
      <b-input v-model="config.flagFormat" @input="onInput"></b-input>
    </b-field>
    <b-field :label="`${$t('event.teamsize')} :`">
      <b-input type="number" v-model.number="config.teamSize" @input="onInput"></b-input>
    </b-field>
    <b-field :label="`${$t('event.state')} :`"></b-field>
    <b-field>
      <b-checkbox v-model="config.visible" @input="onInput">{{$t('event.visible')}}</b-checkbox>
      <b-tooltip :label="$t('event.visible.tooltip')" position="is-right">
        <b-icon icon="help-circle"></b-icon>
      </b-tooltip>
    </b-field>
    <b-field>
      <b-checkbox v-model="config.open" @input="onInput">{{$t('event.open')}}</b-checkbox>
      <b-tooltip :label="$t('event.open.tooltip')" position="is-right">
        <b-icon icon="help-circle"></b-icon>
      </b-tooltip>
    </b-field>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { GeneralEvent } from '../models/generalEvent';

/**
 * Configuration of event general infos
 */
export default Vue.extend({
  name: 'EventGeneralConfig',
  props: {
    config: Object as () => GeneralEvent
  },
  data() {
    return {};
  },
  methods: {
    onInput() {
      this.$emit('input', this.config);
    }
  },
  components: {}
});
</script>

<style lang="scss" scoped>
.b-tooltip {
  margin-left: 1rem;
}
</style>
