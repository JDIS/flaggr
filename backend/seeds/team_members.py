"""Team members seeding data"""

from JDISCTF.models import Team, Participant, TeamMember


def get_records(teams: [Team], participants: [Participant]):
    """Get the records to add to the database"""
    members = []
    captain = True
    for team, participant in zip(teams, participants):
        members.append(TeamMember(team_id=team.id, participant_id=participant.id, captain=captain))
        captain = not captain

    return members


FILTER_ARGS = {'team_id', 'participant_id'}
