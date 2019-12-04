"""Models for SQLAlchemy"""

from JDISCTF.models.category import Category
from JDISCTF.models.challenge import Challenge
from JDISCTF.models.event import Event
from JDISCTF.models.team import Team, TeamMember, TeamRequest
from JDISCTF.models.flag import Flag
from JDISCTF.models.submission import Submission
from JDISCTF.models.user import User
from JDISCTF.models.participant import Participant
from JDISCTF.models.administrator import Administrator, EventAdministrator
from JDISCTF.models.role import RoleAssociation, Role
