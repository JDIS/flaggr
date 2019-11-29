/**
 * Event model
 */
export class Event {
  public id: number;
  public name: string;
  public front_page: string;
  /* True if event is in team, false if its a solo event. Still need to manage teams normally. */
  public teams: boolean;


  constructor(id: number, name: string, front_page: string, teams: boolean) {
    this.id = id
    this.name = name
    this.front_page = front_page
    this.teams = teams
  }
}
