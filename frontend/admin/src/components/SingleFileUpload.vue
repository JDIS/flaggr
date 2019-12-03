<template>
  <div>
    <b-field>
      <b-upload v-model="file" drag-drop @input="$emit('input', file)">
        <div class="drop-zone has-text-centered">
          <b-icon icon="upload" size="is-large"></b-icon>
          <span class="text">{{$t('fileupload')}}</span>
        </div>
      </b-upload>
    </b-field>
    <div v-if="file">
      <span class="tag" :class="`is-${color}`">
        {{file.name}}
        <button class="delete is-small" type="button" @click="removeFile()"></button>
      </span>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

/**
 * Single File Upload
 */
export default Vue.extend({
  name: 'SingleFileUpload',
  props: {
    color: {
      type: String,
      default: 'primary'
    }
  },
  data() {
    return {
      file: null as File | null
    };
  },
  methods: {
    removeFile() {
      this.file = null;
      this.$emit('input', this.file);
    }
  },
  components: {}
});
</script>

<style lang="scss">
.drop-zone {
    display: flex;
    flex-direction: column;
    padding: 2.5rem;
    align-items: center;
    justify-items: center;

    .text {
      max-width: 65%;
    }
}
</style>
