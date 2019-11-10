/**
 * Challenge model
 */
export class Challenge {
  public id: number;
  public name: string;
  public description: string;
  public points: number;
  public solves: string[];
  public files: string[];
  public links: string[];
  public tags: string[];
  public isSolved: boolean;

  constructor() {
    this.id = -1;
    this.name = '';
    this.description = '';
    this.points = 0;
    this.solves = [];
    this.files = [];
    this.links = [];
    this.tags = [];
    this.isSolved = false;
  }
}
