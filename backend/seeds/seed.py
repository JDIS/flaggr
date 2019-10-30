"""Database seeding script and utilities"""

from JDISCTF.app import DB
from typing import List, Generic, TypeVar
from seeds import events, categories, challenges


def seed(verbose: bool = False):
    """Perform seeding for all the tables"""
    db_events = seed_table(events.get_records(), events.FILTER_ARGS, verbose)
    db_categories = seed_table(categories.get_records(db_events), categories.FILTER_ARGS, verbose)
    seed_table(challenges.get_records(db_categories), challenges.FILTER_ARGS, verbose)

    print('Seeding done successfully')


ModelType = TypeVar('ModelType', bound=DB.Model)
ValueType = TypeVar('ValueType', str, int, bool, float)


def seed_table(records: Generic[ModelType], filter_fields: [str], verbose: bool = False) -> \
        List[ModelType]:
    """Seed a single table's data"""
    for record in records:
        filter_args = {field_name: getattr(record, field_name) for field_name in filter_fields}
        rec = DB.session.query(record.__class__).filter_by(**filter_args).first()
        if rec:
            record.id = rec.id
            if verbose:
                print('Record already present: ', record)
        else:
            DB.session.add(record)
            if verbose:
                print('Added record: ', record)

    DB.session.commit()
    return records
