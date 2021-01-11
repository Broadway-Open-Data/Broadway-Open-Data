from sqlalchemy import MetaData
from sqlalchemy.sql.schema import DEFAULT_NAMING_CONVENTION

# Start metadata here and bind later
naming_convention = DEFAULT_NAMING_CONVENTION
metadata = MetaData(naming_convention=naming_convention)
