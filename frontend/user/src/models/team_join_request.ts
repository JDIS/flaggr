import { User } from '@/models/user'
import { Team } from '@/models/team'

/**
 * Model for a request to join a team from a user.
 */
export class TeamJoinRequest {
    public requested_at: string;
    public user: User;
    public team: Team;


    constructor(requested_at: string, user: User, team: Team) {
        this.requested_at = requested_at
        this.user = user
        this.team = team
    }
}
