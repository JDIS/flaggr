<template>
  <b-menu>
    <b-menu-list>
      <b-menu-item
        v-for="link in links"
        v-bind:key="link.name"
        tag="router-link"
        :to="link.url"
        :expanded="isActive(link.url)"
      >
        <template slot="label">
          <div class="menu-item">
            <b-icon :icon="link.icon" :class="`is-${link.color}`"></b-icon>
            <span class="name">{{link.name}}</span>
          </div>
        </template>
        <b-menu-item
          v-for="section in link.sections"
          v-bind:key="section"
          :label="section"
          class="link-section"
        ></b-menu-item>
      </b-menu-item>
    </b-menu-list>
  </b-menu>
</template>

<script lang="ts">
    import Vue from "vue";

    /**
 * Sidebar navigation
 */
export default Vue.extend({
  name: 'AppNavigation',
  data() {
    return {
      links: [
        {
          name: this.$t('event'),
          url: '/event',
          icon: 'trophy',
          sections: [
            this.$t('event.general'),
            this.$t('event.theme'),
            this.$t('event.admins')
          ],
          color: 'first'
        },
        {
          name: this.$t('challenges'),
          url: '/challenges',
          icon: 'flag-variant',
          sections: [],
          color: 'second'
        },
        {
          name: this.$t('participants'),
          url: '/participants',
          icon: 'account-group',
          sections: [],
          color: 'third'
        }
      ]
    };
  },
  methods: {
    isActive(url: string): boolean {
      return this.$route.path.includes(url);
    }
  },
  components: {}
});
</script>

<style lang="scss">
@import '../plugins/buefy-theme.scss';
.menu {
  font-size: 0.9rem;
}
.menu-list {
  .menu-item {
    background-color: $grey-lighter;
    display: flex;
    align-items: center;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 1px;

    .icon {
      padding: 1.75rem;
      border-right-width: 0.2rem;
      border-right-style: solid;
      @extend .colored-border;
    }

    .name {
      padding-left: 1rem;
    }
  }

  li ul {
    padding: 0.5rem 0!important;
  }

  .link-section a {
    padding: 0.5rem 1.5rem;
    font-size: 0.8rem;
  }

  .is-active .menu-item {
    background: repeating-linear-gradient(
        135deg,
        $grey-light,
        $grey-light 10px,
        darken($grey-light, 3%) 10px,
        darken($grey-light, 3%) 20px
      )!important;
  }

  .is-active .menu-item, .menu-item:hover {
    .icon {
      @extend .colored-background;
    }
  }
}
</style>
