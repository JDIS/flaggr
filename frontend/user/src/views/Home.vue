<template>
  <div class="home">
    <div class="front-page" v-html="compiledMarkdown">
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import HelloWorld from '../components/HelloWorld.vue'
import { EventMixin } from '@/mixins/EventMixin'
import marked from 'marked'

/**
 * Homepage
 */
export default Vue.extend({
  name: 'home',
  mixins: [EventMixin],
  components: {
    HelloWorld
  },

  methods: {
    getRenderer() {
      const renderer = new marked.Renderer()
      renderer.paragraph = (text) => {
        return `<span class="paragraph-container"><p>${ text }</p></span>`
      }
      return renderer
    }
  },

  computed: {
    compiledMarkdown() {
      // @ts-ignore
      if (this.event) {
        // @ts-ignore
        return marked(this.event.front_page, { renderer: this.getRenderer(), breaks: true })
      } else {
        return ''
      }
    }
  }
});
</script>

<style scoped lang="scss">
@import "../plugins/buefy-theme.scss";

.front-page {
  margin-top: 1rem;

  /deep/ .paragraph-container {
    width: 100vw;
    background: $dark-1;
    display: block;
    padding: 3rem 0;
    margin-top: 2rem;
    margin-bottom: 2rem;
  }

  /deep/ :not(.paragraph-container) {
    max-width: 1000px;
    margin-left: auto;
    margin-right: auto;
  }

  /deep/ h1 {
    font-size: 200%;
    background: $dark-2;
    text-align: center;
    margin-top: 4rem;
    margin-bottom: 4rem;
  }

  /deep/ p {
    text-align: justify;
  }
}
</style>
