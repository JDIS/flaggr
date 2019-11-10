"""Submissions seeding data"""
from datetime import datetime, timezone

from JDISCTF.models import Challenge, Submission, Team


def get_records(challenges: [Challenge], teams: [Team]):
    """Get the records to add to the database"""
    submissions = []
    for challenge, team in zip(challenges, teams):
        submissions.append(Submission(team_id=team.id, challenge_id=challenge.id, input='flag-123',
                                      is_correct=False,
                                      time=datetime(2019, 9, 24, 18, 0, 0, tzinfo=timezone.utc)))
        submissions.append(Submission(team_id=team.id, challenge_id=challenge.id, input='bépo',
                                      is_correct=True,
                                      time=datetime(2019, 9, 25, 3, 35, 59, tzinfo=timezone.utc)))

    return submissions


FILTER_ARGS = {'team_id', 'challenge_id', 'input'}
