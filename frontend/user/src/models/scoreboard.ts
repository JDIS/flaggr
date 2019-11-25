/**
 * Scoreboard Entry model
 */
export class ScoreboardEntry {
  public team_id: number;
  public team_name: string;
  public points: number;
  public solved_challenges: number;
  public position: number;
  public last_submission: Date;


  constructor(team_id: number, team_name: string, points: number,
              solved_challenges: number, position: number, last_submission: Date) {
    this.team_id = team_id
    this.team_name = team_name
    this.points = points
    this.solved_challenges = solved_challenges
    this.position = position
    this.last_submission = last_submission
  }
}
