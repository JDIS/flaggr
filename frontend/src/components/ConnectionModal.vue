<!-- Modal to sign in or sign up to a competition as a user. -->

<template>
  <div class="connectionModal">
    <div id="top" class="columns">
      <div class="column text is-two-fifths" :class="{active: !isInscription}" id="connection"
           @click="focusCreateTeam()">{{$t('signin')}}</div>
      <b-switch class="column is-flex is-one-fifth" id="switch" v-model="isInscription" :rounded="false"></b-switch>
      <div class="column text is-two-fifths" :class="{active: isInscription}" id="signUp"
           @click="focusJoinTeam()">{{$t('signup')}}</div>
  </div>
    <div id="form">
      <b-field :label="$t('form.usernameOrEmail')" custom-class="is-size-7" label-for="username">
        <b-input placeholder="XxUserxX" size="is-medium" expanded v-model="teamName" id="username"
                 icon="account">
        </b-input>
      </b-field>
      <b-field v-if="isInscription" :label="$t('form.email')" custom-class="is-size-7" label-for="email">
        <b-input placeholder="user@example.org" size="is-medium" expanded v-model="email" id="email"
                 icon="email">
        </b-input>
      </b-field>
      <b-field :label="$t('form.password')" custom-class="is-size-7" label-for="password">
        <b-input type="password" password-reveal placeholder="✱✱✱✱✱✱" size="is-medium" expanded v-model="password" id="password"
                 icon="lock">
        </b-input>
      </b-field>
      <b-field v-if="isInscription" :label="$t('form.passwordConfirmation')" custom-class="is-size-7"
               label-for="password-confirmation">
        <b-input type="password" password-reveal placeholder="✱✱✱✱✱✱" size="is-medium" expanded v-model="passwordConfirmation" id="password-confirmation"
                 icon="lock">
        </b-input>
      </b-field>
      <b-button @click="" type="is-primary" size="is-medium" :icon-right="isInscription ? 'plus-box' : 'arrow-right'">
        <span class="is-flex is-uppercase is-size-6">{{$t(isInscription ? 'signup' : 'signin')}}</span>
      </b-button>
    </div>

  </div>
</template>

<script lang="ts">
  import Vue from 'vue';

  export default Vue.extend({
  name: 'ConnectionModal',
  data() {
    return {
      isInscription: false,
      teamName: '',
      email: '',
      password: '',
      passwordConfirmation: '',
    }
  },
  methods: {
    focusCreateTeam() {
      this.isInscription = false
    },

    focusJoinTeam() {
      this.isInscription = true
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
