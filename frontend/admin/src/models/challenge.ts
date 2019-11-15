import { Track } from './track';

/**
 * Challenge model
 */
export class Challenge {
  public id: number;
  public name: string;
  public description: string;
  public points: number;
  public flag: string;
  public track: Track;
  public hidden: boolean;
  public files: string[];
  public links: string[];
  public tags: string[];

  constructor() {
    this.id = -1;
    this.name = '';
    this.description = '';
    this.points = 0;
    this.flag = '';
    this.track = new Track(-1, '');
    this.hidden = true;
    this.files = [];
    this.links = [];
    this.tags = [];
  }
}
