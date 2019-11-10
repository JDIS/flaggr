<!-- Modal to sign in or sign up to a competition as a user. -->

<template>
  <div class="connectionModal">
    <div id="top" class="columns">
      <div
        class="column text is-two-fifths"
        :class="{ active: !isInscription }"
        id="connection"
        @click="focusCreateTeam()"
      >{{ $t('signin') }}</div>
      <b-switch
        class="column is-flex is-one-fifth"
        id="switch"
        v-model="isInscription"
        :rounded="false"
      ></b-switch>
      <div
        class="column text is-two-fifths"
        :class="{ active: isInscription }"
        id="signUp"
        @click="focusJoinTeam()"
      >{{ $t('signup') }}</div>
    </div>
    <div id="form">
      <b-field
        :label="$t('form.email')"
        custom-class="is-size-7"
        label-for="email"
      >
        <b-input type="email" placeholder="user@example.org" expanded v-model="email" id="email" icon="email"></b-input>
      </b-field>
      <b-field v-show="isInscription" :label="$t('form.username')"
               custom-class="is-size-7" label-for="username">
        <b-input placeholder="XxUserxX" expanded v-model="username" id="username" icon="account"></b-input>
      </b-field>
      <b-field :label="$t('form.password')" custom-class="is-size-7" label-for="password">
        <b-input
          type="password"
          password-reveal
          placeholder="✱✱✱✱✱✱"
          expanded
          v-model="password"
          id="password"
          icon="lock"
        ></b-input>
      </b-field>
      <b-field
        v-show="isInscription"
        :label="$t('form.passwordConfirmation')"
        custom-class="is-size-7"
        label-for="password-confirmation"
      >
        <b-input
          type="password"
          password-reveal
          placeholder="✱✱✱✱✱✱"
          expanded
          v-model="passwordConfirmation"
          id="password-confirmation"
          icon="lock"
        ></b-input>
      </b-field>
      <b-button
        type="is-primary"
        :disabled="isSignupDisabled()"
        :icon-right="isInscription ? 'plus-box' : 'arrow-right'"
        @click="isInscription ? signup() : signin()"
      >{{ $t(isInscription ? "signup" : "signin") }}</b-button>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import store from '../store'

export default Vue.extend({
  name: 'ConnectionModal',
  data() {
    return {
      isInscription: false,
      username: '',
      email: '',
      password: '',
      passwordConfirmation: '',
    }
  },
  methods: {
    signin() {
      store.dispatch('user/connectUser', {email: this.email, password: this.password})
    },

    signup() {
      store.dispatch('user/registerUser', {email: this.email, password: this.password, username: this.username})
    },

    focusCreateTeam() {
      this.isInscription = false
    },

    focusJoinTeam() {
      this.isInscription = true
    },

    isSignupDisabled() {
      return this.isInscription && (this.password === '' || this.password !== this.passwordConfirmation)
    }
  },
  components: {
  }
});
</script>

<style scoped lang="scss">
@import "../style/theme.scss";

#top {
  #switch {
    justify-content: center;
  }

  .active {
    color: $primary-color-light;
    text-decoration: underline;
  }

  .text {
    font-size: 1.2rem;
    cursor: pointer;
  }

  #connection {
    text-align: left;
  }

  #signUp {
    text-align: right;
  }
}
</style>
