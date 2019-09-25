<template>
  <div class="nav-links">
    <router-link :to="{ name: 'home' }" class="navbar-item">Accueil</router-link>
    <router-link :to="{ name: 'challenges' }" class="navbar-item">Défis</router-link>
    <router-link :to="{ name: 'scoreboard' }" class="navbar-item">Scores</router-link>
  </div>
</template>

<script lang="ts">import Vue from 'vue';

export default Vue.extend({
  name: 'NavigationBarLinks',
  components: {
  }
});
</script>

<style scoped lang="scss">
@import "@/style/theme.scss";

.nav-links {
  display: flex;
  align-self: center;

  .navbar-item {
    box-sizing: content-box;
    font-size: 0.8rem;
    font-weight: 300;
    height: 1.25rem;
    margin: 10px;
    padding: 0;
    text-transform: uppercase;

    &:hover,
    &.router-link-exact-active {
      border-bottom: 2px solid $secondary-color;
    }
  }
}

@media screen and (max-width: 1023px) {
  .nav-links {
    display: block;

    .navbar-item {
      max-width: fit-content;
    }
  }
}
</style>