import { Submission } from '@/models/submission'

/**
 * Challenge model
 */
export class Challenge {
  public id: number;
  public name: string;
  public description: string;
  public points: number;
  public files: string[];
  public links: string[];
  public tags: string[];
  public is_solved: boolean;
  public solves: Submission[];

  constructor() {
    this.id = -1;
    this.name = '';
    this.description = '';
    this.points = 0;
    this.files = [];
    this.links = [];
    this.tags = [];
    this.is_solved = false;
    this.solves = [];
  }
}
