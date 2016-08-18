# TimeTracker #

It's an app to let the user able to manage tasks and log work for multiple company and projects.

##Requirements:##
* Python 3.4


## Install Requirements ##
`pip install -r requirements.txt`

##Switch to development branch##
`git checkout develop`

##Run django testcase##
`./manage.py test`

##Migrate the applications##
`./manage.py migrate`

##Load the testing data##
`./manage.py loaddata fixtures/test_data.json`

## Add this to .bash_profile or paste it to terminal ##
```
export TIMETRACKER_DB_NAME='timetracker'
export TIMETRACKER_DB_HOST='root'
export TIMETRACKER_DB_PASSWORD='password'
export TIMETRACKER_DB_PORT='127.0.0.1'
export TIMETRACKER_DB_PORT='5432'
```

## To run testcase ##
`python manage.py test`
