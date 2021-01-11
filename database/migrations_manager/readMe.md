Use this to manage migrations. For fuller documentation, read the [confluence documentation](https://timeadvisors.atlassian.net/wiki/spaces/TAD/pages/316309505/Database+Architecture#Migrations-Manager)



# Making Migrations (Semi-Automated Commands)
Run the following command: `bash database/migrations_manager/run_alembic.sh -m "upgrading this through shell commands" -u -r`
* `-m` is the revision message which will be passed to alembic
* `-u` is an optional flag which will upgrade the db to the current head.
* `-r` is an optional flag which will generate an erd.


# Making Migrations (Individual commands)
1. Navigate to the migrations manager directory (should fix this...) `cd database/migrations_manager`
1. Make the revision `alembic revision --autogenerate -m "My message" `
2. Edit the revision file if necessary _(double check when renaming)_
3. Upgrade with the following: `alembic upgrade head`


---
