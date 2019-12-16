<template>
  <div class="connectionModal">
    <form id="form">
      <b-field
        :label="$t('form.email')"
        custom-class="is-size-7"
        label-for="email"
      >
        <b-input type="email" placeholder="user@example.org"
                 v-on:keyup.enter.native="login()"
                 expanded v-model="email" id="email" icon="email"></b-input>
      </b-field>
      <b-field :label="$t('form.password')" custom-class="is-size-7" label-for="password">
        <b-input
          type="password"
          password-reveal
          placeholder="✱✱✱✱✱✱"
          v-on:keyup.enter.native="login()"
          expanded
          v-model="password"
          id="password"
          icon="lock"
        ></b-input>
      </b-field>
      <b-button
        type="is-success"
        icon-right="arrow-right"
        @click="login()"
      >{{ $t("signin") }}</b-button>
    </form>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import store from '../store'

/**
 * Modal to log in as a admin.
 */
export default Vue.extend({
  name: 'LoginModal',
  data() {
    return {
      email: '',
      password: '',
    }
  },
  methods: {
    login() {
      store.dispatch('admin/connectAdmin', {email: this.email, password: this.password})
    }
  },
  components: {
  }
});
</script>

<style scoped lang="scss">

.button {
  width: 100%;
}

</style>
