"""Team members seeding data"""

from JDISCTF.models import Participant, Team, TeamMember


def get_records_dev(teams: [Team], participants: [Participant]):
    """Get the records to add to the database for development"""
    members = []
    captain = True
    for team, participant in zip(teams, participants):
        members.append(TeamMember(team_id=team.id, participant_id=participant.id, captain=captain))
        captain = not captain

    return members


FILTER_ARGS = {'team_id', 'participant_id'}
