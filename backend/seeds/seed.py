"""Database seeding script and utilities"""

from JDISCTF.app import DB
from typing import List, Generic, TypeVar
from seeds import events


def seed():
    """Perform seeding for all the tables"""
    seed_table(events.get_records(), events.FILTER_ARGS, events.CLASS)


ModelType = TypeVar('ModelType', bound=DB.Model)
ValueType = TypeVar('ValueType', str, int, bool, float)


def seed_table(records: Generic[ModelType], filter_fields: [str], model_class) -> List[ModelType]:
    """Seed a single table's data"""
    for record in records:
        filter_args = {field_name: getattr(record, field_name) for field_name in filter_fields}
        rec = DB.session.query(model_class).filter_by(**filter_args).first()
        if rec:
            record.id = rec.id
        else:
            DB.session.add(record)

    DB.session.commit()
    return records
