<!-- Modal to create or join a team as a user. -->

<template>
  <div class="teamModal">
    <TeamStep1Modal v-if="!this.$store.getters['team/hasTeam']"></TeamStep1Modal>
    <TeamManagementModal v-else></TeamManagementModal>
  </div>
</template>

<script lang="ts">
import Vue from "vue"
import TeamStep1Modal from "@/components/TeamStep1Modal.vue"
import TeamManagementModal from "@/components/TeamManagementModal.vue"

export default Vue.extend({
  name: 'TeamModal',
  data() {
    return {

    }
  },
  methods: {

  },
  components: {
    TeamStep1Modal,
    TeamManagementModal
  }
});
</script>

<style scoped lang="scss">

</style>
