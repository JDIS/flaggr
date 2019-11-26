import {Team} from '@/models/team'
import {Participant} from '@/models/participant';

/**
 * Model for a request to join a team from a participant.
 */
export class TeamJoinRequest {
    public requested_at: string;
    public participant: Participant;
    public team: Team;


    constructor(requested_at: string, participant: Participant, team: Team) {
        this.requested_at = requested_at
        this.participant = participant
        this.team = team
    }
}
