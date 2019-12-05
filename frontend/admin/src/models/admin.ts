import {User} from './user';

/**
 * Model for an admin of the platform.
 */
export class Admin {
    public user: User;
    public id: number;

    constructor(user: User, id: number) {
        this.user = user
        this.id = id
    }
}
