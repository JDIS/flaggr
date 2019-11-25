import { Track } from './track';

/**
 * Challenge model
 */
export class Challenge {
  public id: number;
  public name: string;
  public description: string;
  public points?: number;
  public visible: boolean;
  public flag?: string;
  public track?: Track;
  public files?: string[];
  public links?: string[];
  public tags?: string[];

  constructor() {
    this.id = -1;
    this.name = '';
    this.description = '';
    this.visible = false;
  }
}
