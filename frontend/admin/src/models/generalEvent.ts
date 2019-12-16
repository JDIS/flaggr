/**
 * General Event Configuration
 */
export interface GeneralEvent {
  name: string;
  url: string;
  flagFormat: string;
  teamSize: number;
  is_visible: boolean;
  is_open: boolean;
  /**
   * True if the event is in teams (false if its an event where you participate alone)
   */
  teams: boolean;
}
