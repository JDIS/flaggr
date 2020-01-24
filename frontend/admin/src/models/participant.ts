/**
 * Participant Model
 */
export class Participant {
  id: number;
  user: {
    id: number,
    username: string,
    email: string
  };


  constructor(id: number, user: { id: number; username: string; email: string }) {
    this.id = id;
    this.user = user;
  }
}
