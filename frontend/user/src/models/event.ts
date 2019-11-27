/**
 * Event model
 */
export class Event {
  public id: number;
  public name: string;
  public front_page: string;


  constructor(id: number, name: string, front_page: string) {
    this.id = id
    this.name = name
    this.front_page = front_page
  }
}
