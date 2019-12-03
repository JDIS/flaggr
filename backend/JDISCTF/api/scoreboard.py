"""Scoreboard routes"""

from sqlalchemy import text

from JDISCTF.app import DB, REGISTRY
from JDISCTF.models import Event
from JDISCTF.permission_wrappers import require_event
from JDISCTF.schemas.scoreboard import ScoreboardSchema


@REGISTRY.handles(
    rule="/event/<int:event_id>/scoreboard",
    method="GET",
    response_body_schema=ScoreboardSchema(many=True)
)
@require_event
def get_scoreboard(event: Event):
    """Get the scoreboard data"""

    query = """
    SELECT ROW_NUMBER() OVER (ORDER BY qq.pointss DESC) AS "position",
       qq.team_id, qq.pointss AS points, qq.team_name, qq.last_submission, qq.solved_challenges
    FROM (
    SELECT team_id, SUM(points) AS "pointss", team_name, MAX(submission_time) AS "last_submission", COUNT(challenge_id) as "solved_challenges"
    FROM (
        SELECT DISTINCT ON (s.challenge_id, s.team_id)
             s.team_id AS "team_id", t.name AS "team_name",
           s.challenge_id AS "challenge_id", c.points as "points", s.time AS "submission_time"
        FROM "Submissions" s
        JOIN "Teams" t ON t.id = s.team_id
        JOIN "Challenges" c on c.id = s.challenge_id
        WHERE s.is_correct = true
            AND t.event_id = :e
    ) AS q
    GROUP BY q.team_id, q.team_name
    ) as qq
    ORDER BY pointss DESC
    """

    result = list(DB.engine.execute(text(query), e=event.id))
    return list(map(dict, result))
