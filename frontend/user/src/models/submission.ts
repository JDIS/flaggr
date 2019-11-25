import { Team } from '@/models/team'

/**
 * Submission model for when a flag is submitted.
 */
export class Submission {
  public input: string;
  public time: string;
  public is_correct: boolean;
  public team: Team | any;


  constructor(input: string, time: string, is_correct: boolean, team: Team | unknown = null) {
    this.input = input
    this.time = time
    this.is_correct = is_correct
    this.team = team
  }
}
