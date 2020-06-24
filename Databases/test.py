from db import db
import datetime
import uuid

# ------------------------------------------------------------------------------
now = datetime.datetime.utcnow()

my_show = db.Show(
    id=str(uuid.uuid4()),
    date_instantiated=now,
)
db.session.add(my_show)
del my_show
db.session.commit()

my_theatre = Theatre(
    id=str(uuid.uuid4()),
    date_instantiated=now,
)
db.session.add(my_theatre)
del my_theatre
db.session.commit()

print("Completed!")
