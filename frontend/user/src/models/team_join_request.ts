import { User } from '@/models/user'

/**
 * Model for a request to join a team from a user.
 */
export class TeamJoinRequest {
    public requested_at: string;
    public user: User;


    constructor(requested_at: string, user: User) {
        this.requested_at = requested_at
        this.user = user
    }
}
