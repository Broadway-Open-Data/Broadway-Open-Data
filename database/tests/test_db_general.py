import sys
import os


if os.environ.get('PROJECT_PATH'):
    sys.path.append(os.environ.get('PROJECT_PATH'))
else:
    sys.path.append('database')



from database.models.shows import Show
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, YEAR



def test_show_schema():
    """
    Tests and asserts that model.show contains required fields.
    """

    show_fields = {x.name:x.type for x in Show.__table__.c}

    expected_show_fields = {
        'id': Integer(),
        'date_instantiated': DateTime(),
        'title': String(length=200),
        'opening_date': DateTime(),
        'closing_date': DateTime(),
        'previews_date': DateTime(),
        'year': YEAR(),
        'theatre_id': Integer(),
        'scraped_theatre_name': String(length=60),
        'production_type': String(length=20),
        'show_type': String(length=20),
        'show_type_simple': String(length=20),
        'intermissions': TINYINT(),
        'n_performances': Integer(),
        'run_time': Integer(),
        'show_never_opened': Boolean(),
        'revival': Boolean(),
        'pre_broadway': Boolean(),
        'limited_run': Boolean(),
        'repertory': Boolean(),
        'other_titles': String(length=300),
        'official_website': String(length=100)
    }


    for key, value in expected_show_fields.items():
        assert type(show_fields[key]) == type(value)


if __nam__ == '__main__':
    test_show_schema()
