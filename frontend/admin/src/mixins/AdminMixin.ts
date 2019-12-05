import store from '../store'
import {Admin} from '@/models/admin';

/**
 * Use this mixin to have access to the connected admin.
 */
export const AdminMixin = {
  computed: {
    admin(): Admin {
      return (store.state as any).admin.connectedAdmin as Admin
    }
  },

  methods: {
    isConnected(): boolean {
      return store.getters['admin/isConnected']
    }
  }
}
