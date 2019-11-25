"""Database seeding script and utilities"""

from typing import Generic, List, TypeVar

from JDISCTF.app import DB
from seeds import categories, challenges, events, flags, submissions, teams, users, participants

ModelType = TypeVar('ModelType', bound=DB.Model)
ValueType = TypeVar('ValueType', str, int, bool, float)


class Seeder:
    """Utility class for seeding the database"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def seed(self):
        """Perform seeding for all the tables"""

        print(f'Database URL: {DB.engine.url}')

        db_events = self.seed_table(events.get_records(), events.FILTER_ARGS)
        db_categories = self.seed_table(categories.get_records(db_events), categories.FILTER_ARGS)
        db_challenges = self.seed_table(challenges.get_records(db_categories),
                                        challenges.FILTER_ARGS)
        self.seed_table(flags.get_records(db_challenges), flags.FILTER_ARGS)
        db_teams = self.seed_table(teams.get_records(db_events), teams.FILTER_ARGS)
        self.seed_table(submissions.get_records(db_challenges, db_teams), submissions.FILTER_ARGS)

        db_users = self.seed_table(users.get_records(db_events), users.FILTER_ARGS)

        self.seed_table(participants.get_records(db_users, db_events), participants.FILTER_ARGS)

        print('Seeding done successfully')

    def seed_table(self, records: Generic[ModelType], filter_fields: [str]) -> List[ModelType]:
        """Seed a single table's data"""
        for record in records:
            filter_args = {field_name: getattr(record, field_name) for field_name in filter_fields}
            rec = DB.session.query(record.__class__).filter_by(**filter_args).first()
            if rec:
                record.id = rec.id
                if self.verbose:
                    print('Record already present: ', record)
            else:
                DB.session.add(record)
                if self.verbose:
                    print('Added record: ', record)

        DB.session.commit()
        return records
