<!-- Modal to create or join a team as a user. -->

<template>
  <div class="teamModal">
    <TeamRequestStatusModal v-if="hasPendingRequest()" :request="teamRequest">yes</TeamRequestStatusModal>
    <TeamStep1Modal v-else-if="!hasTeam()"></TeamStep1Modal>
    <TeamManagementModal v-else></TeamManagementModal>
  </div>
</template>

<script lang="ts">
import Vue from "vue"
import TeamStep1Modal from "@/components/TeamStep1Modal.vue"
import TeamManagementModal from "@/components/TeamManagementModal.vue"
import { TeamMixin } from "@/mixins/TeamMixin"
import TeamRequestStatusModal from "@/components/TeamRequestStatusModal.vue"

export default Vue.extend({
  name: 'TeamModal',
  mixins: [TeamMixin],
  data() {
    return {

    }
  },
  methods: {

  },
  components: {
    TeamStep1Modal,
    TeamManagementModal,
    TeamRequestStatusModal
  }
});
</script>

<style scoped lang="scss">

</style>
