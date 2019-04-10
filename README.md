# Jobs for Hope
Aggregate job opportunities with homeless service providers so that people can search for a job that fits their skillset.

## Full-Stack React/Node Application Installation
1. Clone this repo to your local drive.
2. Change to the jobs-for-hope directory:
```
cd jobs-for-hope
```
3. Install the node server npm depedencies:
```
npm install
```
4. Obtain the ```.env``` file from the slack channel and place it in this directory. It contains private info (i.e., the production database connection string) that we cannot put in this public GitHub repo.
4. Change to the client directory:
```
cd client
```
5. Install the client (React) dependencies:
```
npm install
```
## To Run the React/Node Application
1. Run ```npm start``` from the jobs-for-hope directory to start the node server.
2. Run ```npm start``` from the jobs-for-hope/client directory to start the react app and open the browser.


## Backend Python Scraper Setup
1. Download the required software for the project

        brew install python@2 git

- Python 2.7 (https://www.python.org/downloads/release/python-2715/)
- Git (https://git-scm.com/downloads) GUI Add-Ons(https://git-scm.com/downloads/guis)

2. Install virtualenv using pip

        pip install virtualenv virtualenvwrapper

3. Find virtualenvwrapper.sh location

        which virtualenvwrapper.sh

4. Create directory to hold virtual environments

        mkdir $HOME/.virtualenvs

5. Add to .bash_profile

        export WORKON_HOME=$HOME/.virtualenvs
        source /path/to/virtualenwrapper.sh

6. Create the virtualenv

        source ~/.bashrc  // activate virtualenvwrapper.sh, just for the first time
        mkvirtualenv jobs-for-hope
        mkvirtualenv -p /usr/local/bin/path/to/python2.7 jobs-for-hope  // use this if the system default is python3

7. Activate the virtualenv

        workon  // list the existing virtual environments, blank if none is created
        workon jobs-for-hope  // activate virtual environment, not needed when first creating the virtualenv

8. Install project dependencies

        pip install -r ./requirements.txt

9. Work on the scraper and run

        python jfh_scraper.py

9. Deactivate the virtualenv

        deactivate  // switch back to system python

## Checking the database for scraped data

1. Install sqlite

        brew install sqlite

2. Make sure the db file is there

        ls -l jobs_for_hope.db

3. Open the database environment (Ctrl-D to exit)

        sqlite3 jobs_for_hope.db

4. Print the db schema

        .schema

5. Print the jobs table row count

        select count(*) from jobs;

6. Print all the jobs

        select * from jobs;

7. Exit db. Press Ctrl-D

## Project Structure
1. app.py: This is the main entrypoint into the application that contains the routes and associated business logic. This file also contains the main instantiation of the app object
2. api.py: This is the main class for the REST API that allows interaction with the database
3. backend/requirements.txt: This is the file that contains all of the projects backend dependencies. Pip looks inside here when it installs all dependencies
3. backend/jfh_scraper.py: This is the scraper which parses websites for jobs data and stores them in an sqlite database
4. readme.md: This is the file that contains all instructions and descriptions about jobs-for-hope
5. static folder: This folder contains all of the Javascript and CSS content. Place all JS and CSS into their respective folders.
6. templates folder: This folder contains all of the html templates that are rendered by the application. All Jinjas2 and HTML templates go here.
7. utilities folder: This folder contains all of the helper tools used to write and read data to and from the database. It also contains utility scripts used for the application

## Branches
1. master: main stable branch with frontend and backend getting data from a temporary spreadsheet
2. seleniumscrapers: development branch for the python scraper
3. db_backend: development branch which integrates the frontend with the backend api using real data from the sqlite database


## Contributing
