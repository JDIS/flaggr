/**
 * Flag model. A flag is an answer to a challenge, can be a regex or a static string.
 */
export class Flag {
  public id: number = 0;
  public value: string = '';
  public challenge_id: number = 0;
  public is_regex: boolean = false;
}
