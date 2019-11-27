<template>
  <b-field :label="`${$t('challenge.tags')} :`">
    <b-taginput
      v-model="selectedTags"
      :data="availableTags"
      autocomplete
      allow-new
      open-on-focus
      @typing="getFilteredTags"
      @input="changeTags"
    ></b-taginput>
  </b-field>
</template>

<script lang="ts">
import Vue from 'vue';

/**
 * Input for choosing tags from existing list or add new ones
 */
export default Vue.extend({
  name: 'ChallengeTagInput',
  props: {},
  data() {
    return {
      tags: [] as string[],
      selectedTags: [] as string[]
    };
  },
  created() {
    this.tags = ['bla', 'blabla']; // TODO: get existing tags from API
  },
  methods: {
    /* Filters tags based on the current user input */
    getFilteredTags(input: string): string[] {
      return this.availableTags.filter((tag) => {
        return tag.toLowerCase().indexOf(input.toLowerCase()) >= 0;
      });
    },
    changeTags() {
      this.$emit('tagsChange', this.selectedTags);
    }
  },
  computed: {
    availableTags(): string[] {
      return this.tags.filter((tag) => !this.selectedTags.includes(tag));
    }
  }
});
</script>

<style lang="scss">

</style>
