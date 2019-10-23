import { Challenge } from '../models/challenge';

/**
 * API service for Challenges
 */
/**
 * Get the challenge list
 * @returns {Challenge[]}
 */
export function getChallenges(): Challenge[] {
  // TODO: get from API
  return [
    new Challenge('On joue à cache cache?',
      'On a vu ce charmant formulaire dont on ne comprends pas trop ce qu\'il fait. On est vraiment perplexe face au fait qu\'on voit seulement un bouton, mais qu\'il y a de l\'interaction de la part du formulaire.',
      75,
      'web',
      10,
      [],
      ['https://cachecache.unitedctf.ca/'],
      ['something', 'something else', 'another']
    ),
    new Challenge('The Lost Park',
      'What is the name of this monument?',
      100,
      'crypto',
      3,
      ['statue.jpg'],
      [],
      ['something'],
      true
    )
  ];
}
