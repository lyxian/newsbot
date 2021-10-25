# AIRFLOW (local) for NewsBot

## DONE

- setup repo
- add shortCircuit for "working hours" (12am - 9am)
- add method to remove duplicates in `list of dictionary`
- error handling for non-unique inputs << use set
- incorrectly sorted articles after set << sort after set
- fix daemon airflow server (rm airflow files)
- refactor article sorting and addition

## TO-DO

- run dag based on TIME (current & previous) + practise using templates/jinjja
- add pytest -> unit-test
- deploy to AWS
- how to upgrade existing airflow version
- ***
- improve Telegram message
- query USER from cloud
- host subscription bot on cloud && setup DB there (!!scripting cloud telebot)
- error bot + telegram msg error handling

# PAUSED TO COMPLETE TELEBOT ON CLOUD

#Packages
wheel
apache-airflow
bs4
psycopg2-binary
pyTelegramBotAPI
#Packages

query.order_by( <table>.<column>.asc/desc() )
