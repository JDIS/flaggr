import {Track} from './track';
import {Flag} from '@/models/flag';

/**
 * Challenge model
 */
export class Challenge {
  public id: number;
  public name: string;
  public description: string;
  public points?: number;
  public visible: boolean;
  public flags?: Flag[];
  public track?: Track;
  public files?: File[];
  public links?: string[];
  public tags?: string[];

  constructor() {
    this.id = -1;
    this.name = '';
    this.description = '';
    this.visible = false;
    this.files = [];
    this.links = [];
    this.tags = [];
    this.flags = [new Flag()];
  }
}
