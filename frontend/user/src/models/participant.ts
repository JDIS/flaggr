import {User} from './user';

/**
 * Model for a participant of a competition.
 */
export class Participant {
    public user: User;
    public id: number;

    constructor(user: User, id: number) {
        this.user = user
        this.id = id
    }
}
