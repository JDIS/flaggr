<template>
  <div>
    <b-field>
      <b-upload v-model="files" multiple drag-drop @input="$emit('input', files)">
        <div class="drop-zone has-text-centered">
          <b-icon icon="upload" size="is-large"></b-icon>
          <span class="text">{{$t('fileupload')}}</span>
        </div>
      </b-upload>
    </b-field>
    <div class="tags">
      <span v-for="(file, index) in files" :key="index" class="tag" :class="`is-${color}`">
        {{file.name}}
        <button class="delete is-small" type="button" @click="removeFile(index)"></button>
      </span>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

/**
 * Multiple File Upload
 */
export default Vue.extend({
  name: 'MultipleFileUpload',
  props: {
    color: {
      type: String,
      default: 'primary'
    }
  },
  data() {
    return {
      files: [] as File[]
    };
  },
  methods: {
    removeFile(index: number) {
      this.files.splice(index, 1);
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
