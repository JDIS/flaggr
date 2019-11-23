<template>
  <div class="nav-links">
    <router-link :to="{ name: 'home' }" class="navbar-item">{{ $t('title.home') }}</router-link>
    <router-link :to="{ name: 'challenges' }" v-if="isConnected && hasTeam" class="navbar-item">{{ $t('title.challenges') }}</router-link>
    <router-link :to="{ name: 'scoreboard' }" class="navbar-item">{{ $t('title.scoreboard') }}</router-link>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { UserMixin } from '@/mixins/UserMixin'
import Router from 'vue-router'
import router from '@/router'
import { TeamMixin } from '@/mixins/TeamMixin'


export default Vue.extend({
  name: 'NavigationBarLinks',
  mixins: [UserMixin, TeamMixin],
  data() {
    return {
      routes: null as unknown as Router
    }
  },
  mounted() {
    this.routes = router
  },
  components: {
  },
  methods: {
  }
});
</script>

<style scoped lang="scss">
@import "../style/theme.scss";

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

@media screen and (max-width: 768px) {
  .nav-links {
    display: block;

    .navbar-item {
      max-width: fit-content;
    }
  }
}
</style>
