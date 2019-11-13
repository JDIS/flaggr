import { User } from '@/models/user'

/**
 * Model for a member of a team.
 */
export class TeamMember {
    public captain: boolean;
    public user: User;


    constructor(captain: boolean, user: User) {
        this.captain = captain
        this.user = user
    }
}
