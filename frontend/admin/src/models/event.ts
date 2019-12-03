import { GeneralEvent } from './generalEvent';
import { EventTheme } from './eventTheme';

/**
 * Event Model
 */
export class Event implements GeneralEvent, EventTheme {
  id: number;
  name: string;
  url: string;
  flagFormat: string;
  teamSize: number;
  visible: boolean;
  open: boolean;
  customCSS: string;
  homePage: string;
  logo?: File;

  constructor() {
    this.id = -1;
    this.name = '';
    this.url = '';
    this.flagFormat = '';
    this.teamSize = 4;
    this.visible = false;
    this.open = false;
    this.customCSS = '';
    this.homePage = '';
  }
}
