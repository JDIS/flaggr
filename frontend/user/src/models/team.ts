import { TeamMember } from '@/models/team_member'

/**
 * Model for a team. Team contains users and a captain, and requests to join.
 */
export class Team {
    public name: string;
    public event_id: number;
    public id: number;
    public members: TeamMember[]

    constructor(name: string, event_id: number, id: number, members: TeamMember[]) {
        this.name = name
        this.event_id = event_id
        this.id = id
        this.members = members
    }
}
