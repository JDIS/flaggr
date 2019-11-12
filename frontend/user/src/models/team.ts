import { User } from '@/models/user'

/**
 * Model for a team. Team contains users and a captain, and requests to join.
 */
export class Team {
    public name: string;
    public event_id: number;
    public id: number;
    public members: {captain: boolean, users: User[]}

    constructor(name: string, event_id: number, id: number, members: { captain: boolean; users: User[] }) {
        this.name = name
        this.event_id = event_id
        this.id = id
        this.members = members
    }
}
