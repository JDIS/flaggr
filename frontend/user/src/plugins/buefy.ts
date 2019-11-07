import Vue from 'vue';
import Buefy from 'buefy';

// https://buefy.org/documentation/constructor-options
Vue.use(Buefy, {
    defaultIconPack: 'mdi-light',
    defaultTooltipType: 'is-dark',
    customIconPacks: {
        'mdi-light': {
            sizes: {
                'default': '',
                'is-small': 'mdi-18px',
                'is-medium': 'mdi-24px',
                'is-large': 'mdi-48px'
            },
            iconPrefix: 'mdi mdi-'
        }
    }
});

