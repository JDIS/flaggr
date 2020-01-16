import {GeneralEvent} from './generalEvent';
import {EventTheme} from './eventTheme';

/**
 * Event Model
 */
export class Event implements GeneralEvent, EventTheme {
  id: number;
  name: string;
  url: string;
  flagFormat: string;
  teamSize: number;
  is_visible: boolean;
  is_open: boolean;
  customCSS: string;
  front_page: string;
  logo?: File;
  /**
   * True if the event is in teams (false if its an event where you participate alone)
   */
  teams: boolean;

  constructor() {
    this.id = -1;
    this.name = '';
    this.url = '';
    this.flagFormat = '';
    this.teamSize = 4;
    this.is_visible = false;
    this.is_open = false;
    this.customCSS = '';
    this.front_page = '';
    this.teams = false;
  }
}
