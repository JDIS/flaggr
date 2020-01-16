<template>
  <div>
    <b-field :label="`${$t('event.name')} :`">
      <b-input v-model="config.name" @input="onInput"></b-input>
    </b-field>
    <b-field :label="`${$t('event.frontPage')} :`"></b-field>
    <b-switch v-model="preview" type="is-success" :rounded="false">{{ $t('preview') }}</b-switch>
    <b-input v-if="!preview" v-model="config.front_page" @input="onInput" type="textarea"></b-input>
    <div v-else class="front-page" v-html="compiledMarkdown"></div>
    <b-field :label="`${$t('event.url')} :`" v-if="false"> <!-- Unsupported for now -->
      <b-input v-model="config.url" @input="onInput"></b-input>
    </b-field>
    <b-field :label="`${$t('event.flagformat')} :`" v-if="false"> <!-- Unsupported for now -->
      <b-input v-model="config.flagFormat" @input="onInput"></b-input>
    </b-field>
    <b-field :label="`${$t('event.teamsize')} :`" v-if="false"> <!-- Unsupported for now -->
      <b-input type="number" v-model.number="config.teamSize" @input="onInput"></b-input>
    </b-field>
    <b-field>
      <b-checkbox v-model="config.teams" @input="onInput">{{$t('event.teams')}}</b-checkbox>
      <b-tooltip :label="$t('event.teams.tooltip')" position="is-right">
        <b-icon icon="help-circle"></b-icon>
      </b-tooltip>
    </b-field>
    <b-field :label="`${$t('event.state')} :`"></b-field>
    <b-field>
      <b-checkbox v-model="config.is_visible" @input="onInput">{{$t('event.visible')}}</b-checkbox>
      <b-tooltip :label="$t('event.visible.tooltip')" position="is-right">
        <b-icon icon="help-circle"></b-icon>
      </b-tooltip>
    </b-field>
    <b-field>
      <b-checkbox v-model="config.is_open" @input="onInput">{{$t('event.open')}}</b-checkbox>
      <b-tooltip :label="$t('event.open.tooltip')" position="is-right">
        <b-icon icon="help-circle"></b-icon>
      </b-tooltip>
    </b-field>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import {GeneralEvent} from '@/models/generalEvent';
import marked from 'marked'

/**
 * Configuration of event general infos
 */
export default Vue.extend({
  name: 'EventGeneralConfig',
  props: {
    config: Object as () => GeneralEvent
  },
  data() {
    return {
      preview: false
    };
  },
  computed: {
    compiledMarkdown() {
      // @ts-ignore
      if (this.config) {
        // @ts-ignore
        return marked(this.config.front_page, { renderer: this.getRenderer(), breaks: true })
      } else {
        return ''
      }
    }
  },
  methods: {
    getRenderer() {
      const renderer = new marked.Renderer()
      renderer.paragraph = (text) => {
        return `<span class="paragraph-container"><p>${ text }</p></span>`
      }
      return renderer
    },

    onInput() {
      // @ts-ignore
      this.$emit('input', this.config);
    }
  },
  components: {}
});
</script>

<style lang="scss" scoped>
@import "../plugins/buefy-theme.scss";

.b-tooltip {
  margin-left: 1rem;
}
.front-page {
  margin-top: 1rem;

  /deep/ .paragraph-container {
    width: 100%;
    background: #DDD;
    display: block;
    padding: 3rem 0;
    margin-top: 2rem;
    margin-bottom: 2rem;
  }

  /deep/ :not(.paragraph-container) {
    max-width: 80%;
    margin-left: auto;
    margin-right: auto;
  }

  /deep/ h1 {
    font-size: 200%;
    background: #AAA;
    text-align: center;
    margin-top: 4rem;
    margin-bottom: 4rem;
  }

  /deep/ p {
    text-align: justify;
  }
}

</style>
