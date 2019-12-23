"""Database seeding script and utilities"""

import os
import secrets
from typing import Generic, List, TypeVar

from JDISCTF.app import DB
from JDISCTF.models import Administrator, User
from seeds import admins, categories, challenges, event_administrators, events, flags, participants, \
    submissions, team_members, teams, users

ModelType = TypeVar('ModelType', bound=DB.Model)
ValueType = TypeVar('ValueType', str, int, bool, float)


def seed_users(user_records: [User]):
    """
    Seed the users into the database.

    Users have to be handled separately because we want each event to have the same participants (same email and
    username) to simplify testing, but the generic seeding method doesn't allow that.
    """
    users_count = User.query.count()
    if users_count < len(user_records):
        for user in user_records[:len(user_records) - users_count]:
            DB.session.add(user)

        DB.session.commit()

    return User.query.all()


class Seeder:
    """Utility class for seeding the database"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def seed(self):
        """Perform seeding for all the tables"""

        print(f'Database URL: {DB.engine.url}')
        print(f'Environment: {os.environ.get("FLASK_ENV")}')

        if os.environ.get('FLASK_ENV') == 'development':

            db_events = self.seed_table(events.get_records_dev(), events.FILTER_ARGS)
            db_categories = self.seed_table(categories.get_records_dev(db_events), categories.FILTER_ARGS)
            db_challenges = self.seed_table(challenges.get_records_dev(db_categories),
                                            challenges.FILTER_ARGS)
            self.seed_table(flags.get_records_dev(db_challenges), flags.FILTER_ARGS)
            db_teams = self.seed_table(teams.get_records_dev(db_events), teams.FILTER_ARGS)
            self.seed_table(submissions.get_records_dev(db_challenges, db_teams), submissions.FILTER_ARGS)

            db_users = seed_users(users.get_records_dev(db_events))

            db_participants = self.seed_table(participants.get_records_dev(db_users, db_events),
                                              participants.FILTER_ARGS)

            self.seed_table(team_members.get_records_dev(db_teams, db_participants), team_members.FILTER_ARGS)

            db_admins = self.seed_table(admins.get_records_dev(db_users), admins.FILTER_ARGS)
            self.seed_table(event_administrators.get_records_dev(db_admins, db_events),
                            event_administrators.FILTER_ARGS)

        elif os.environ.get('FLASK_ENV') == "production":
            admin_list = Administrator.query.all()
            if len(admin_list) == 0:
                admin_email = 'admin@admin.com'
                admin_password = secrets.token_hex()
                admin_user = User(id=0, email=admin_email, username='admin')
                print("")
                print("")
                print("")
                print("==================================================================")
                print("========================ADMIN EMAIL===============================")
                print(admin_email)
                print("=======================ADMIN PASSWORD=============================")
                print(admin_password)
                print("=======================ADMIN PASSWORD=============================")
                print("========TAKE NOTE OF THIS, IT WON'T BE PRINTED ANOTHER TIME=======")
                print("==================================================================")
                print("")
                print("")
                print("")
                admin_user.set_password(admin_password)

                admin_admin = Administrator(id=0, is_platform_admin=True, user=admin_user)

                DB.session.add(admin_admin)
                DB.session.commit()
            else:
                print("There is already an admin, not seeding another admin.")

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
