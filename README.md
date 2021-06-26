# AIRFLOW (local) for NewsBot

## TO-DO

- setup repo
- add shortCircuit for "working hours"
- improve Telegram message
- host subscription bot on cloud

##

airflow connection add <conn_id> \
--conn-type sqlite
--conn-host $PWD/test.db

#Packages
wheel
apache-airflow
bs4
psycopg2-binary
pyTelegramBotAPI
#Packages

query.order_by( <table>.<column>.asc/desc() )
