Helpful stuff for this database.

## Database Management
To restart local db:
`pg_ctl -D /usr/local/var/ta_2.0 start`

# Migrations
To run alembic migrations, execute from project root with the following:
  `alembic -c database/migrations_manager/alembic.ini revision`

Because this can be a lot, I've created an automated migrations script. Use it
as follows:
  `bash database/migrations_manager/run_alembic.sh -m "Message" -u -r`
* `-m` is the migration message (like git commit message)
* `-u` is a flag to upgrade.
* `-r` is a flag to generate an erd.
For further details, read the docs in [database/migrations_manager](migrations_manager/)
