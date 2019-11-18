/**
 * Model for a challenge track (category)
 */
export class Track {
  public id: number;
  public name: string;

  constructor(id: number, name: string) {
      this.id = id;
      this.name = name;
  }
}
