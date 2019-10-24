"""Database seeding script and utilities"""

from JDISCTF.app import DB
from typing import List, Generic, TypeVar
from seeds import events, categories, challenges, flags, submissions, teams


_verbose = False


def seed(verbose: bool = False):
    """Perform seeding for all the tables"""
    global _verbose
    _verbose = verbose

    print(f'Database URL: {DB.engine.url}')

    db_events = seed_table(events.get_records(), events.FILTER_ARGS)
    db_categories = seed_table(categories.get_records(db_events), categories.FILTER_ARGS)
    db_challenges = seed_table(challenges.get_records(db_categories), challenges.FILTER_ARGS)
    seed_table(flags.get_records(db_challenges), flags.FILTER_ARGS)
    db_teams = seed_table(teams.get_records(db_events), teams.FILTER_ARGS)
    seed_table(submissions.get_records(db_challenges, db_teams), submissions.FILTER_ARGS)

    print('Seeding done successfully')


ModelType = TypeVar('ModelType', bound=DB.Model)
ValueType = TypeVar('ValueType', str, int, bool, float)


def seed_table(records: Generic[ModelType], filter_fields: [str]) -> \
        List[ModelType]:
    """Seed a single table's data"""
    for record in records:
        filter_args = {field_name: getattr(record, field_name) for field_name in filter_fields}
        rec = DB.session.query(record.__class__).filter_by(**filter_args).first()
        if rec:
            record.id = rec.id
            if _verbose:
                print('Record already present: ', record)
        else:
            DB.session.add(record)
            if _verbose:
                print('Added record: ', record)

    DB.session.commit()
    return records
