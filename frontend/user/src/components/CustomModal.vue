<template>
  <div class="modalComponent">
    <div id="invisible" @click="sendCloseEvent()"></div>
    <div class="modalInnerComponent">
      <div id="modalTip">
        <div id="triangle1"></div>
        <div id="triangle2"></div>
      </div>
      <div class="modalContent">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

/**
 * Generic Modal to display stuff over other stuff
 */
export default Vue.extend({
  name: 'CustomModal',
  props: ['visible'],
  data() {
    return {}
  },
  methods: {
    sendCloseEvent() {
      this.$emit('close')
    }
  },
  components: {}
});
</script>

<style scoped lang="scss">
@import "../style/theme.scss";

$top-offset: 5rem;

.modalInnerComponent {
  box-shadow: 0 0 3px black;
  position: absolute;
  top: $top-offset;
  left: -13rem;
  width: 22rem;

  padding: 1rem;
  background: $dark-2;
  border-radius: 0.3rem;
  z-index:100;

}

#invisible {
  position: fixed;
  width: 1000vw;
  height: 1000vh;
  top: 0;
  left: 0;
  z-index: 100 !important;
}

#modalTip {
  width: 3rem;
  height: 1rem;
  position:absolute;
  top: -1.27rem;
  right: 5rem;

  $rotation: 38deg;
  $background: $dark-2;
  #triangle1 {
    border-top: 1px solid black;
    width: 2rem;
    height: 1rem;
    background: $background;
    transform: rotate(-$rotation);
    position: absolute;
    bottom: -0.5rem;
  }

  #triangle2 {
    border-top: 1px solid black;
    width: 2rem;
    height: 1rem;
    background: $background;
    transform: rotate($rotation);
    position: absolute;
    right:0;
    bottom: -0.5rem;
  }
}
</style>
