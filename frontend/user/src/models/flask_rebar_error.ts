/**
 * Model for an error sent by flask-rebar.
 */
export class FlaskRebarError {
    public message: string;

    constructor(message: string) {
        this.message = message;
    }
}
