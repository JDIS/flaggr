/**
 * Challenge model
 */
export class Challenge {
  public name: string;
  public description: string;
  public points: number;
  public track: string;
  public solves: number;
  public files: string[];
  public links: string[];
  public tags: string[];
  public isSolved: boolean;

  constructor(name: string, description: string, points: number, track: string, solves: number, files: string[] = [],
              links: string[] = [], tags: string[] = [], isSolved: boolean = false) {
    this.name = name;
    this.description = description;
    this.points = points;
    this.track = track;
    this.solves = solves;
    this.files = files;
    this.links = links;
    this.tags = tags;
    this.isSolved = isSolved;
  }
}
