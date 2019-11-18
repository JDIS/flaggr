import {Participant} from '@/models/participant';

/**
 * Model for a member of a team.
 */
export class TeamMember {
    public captain: boolean;
    public participant: Participant;


    constructor(captain: boolean, participant: Participant) {
        this.captain = captain
        this.participant = participant
    }
}
