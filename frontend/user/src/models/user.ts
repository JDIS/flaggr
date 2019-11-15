/**
 * Model for a user who participates in a competition.
 */
export class User {
    public username: string;
    public email: string;
    public id: number;

    constructor(username: string, email: string, id: number) {
        this.username = username
        this.email = email
        this.id = id
    }
}
