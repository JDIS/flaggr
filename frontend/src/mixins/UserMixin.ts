import { User } from '@/models/user'
import store from '../store'

/**
 * Use this mixin to have access to the connected user.
 */
export const UserMixin = {
  computed: {
    user() {
      return (store.state as any).user.connectedUser as User
    }
  }
}
