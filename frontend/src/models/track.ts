import { Challenge } from './challenge';

/**
 * Model for a challenge track (category)
 */
export class Track {
  public id: number;
  public name: string;
  public challenges: Challenge[];

  constructor(id: number, name: string, challenges: Challenge[]) {
      this.id = id;
      this.name = name;
      this.challenges = challenges;
  }
}
