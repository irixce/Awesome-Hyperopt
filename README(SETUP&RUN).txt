# Steps to set up the environment

1 Open terminal at awesome-hyperopt folder and create virtual environment.
2 Activate virtual enviroment then
    $ pip install -r requirement.txt
    $ cd client
    $ npm install
3 Follow steps for database. (If you already have PostgreSQL installed then start from step 4)



# Steps to install PostgreSQL

1 Go to https://www.postgresql.org/download/
2 Select OS
* Mac
    - download postgress.app, follow instructions.
	- from terminal and in venv, type the following command:
	    (venv)$ PATH=$PATH:/Applications/Postgres.app/Contents/Versions/11/bin pip install psycopg2
* Windows
	- From command, type the following instruction $ pip install psycopg2
3 Go to https://www.pgadmin.org/ and download pgadmin4
4 Open pgadmin4 on your computer.
    - Right click 'servers' -> Create -> Server
    - Name: test
    - Connection tab, Host name/address: localhost -> save
    - THEN
    - expand test -> expand Databases -> Right click db -> Properties...
    - Security tab -> Privileges
        ** Is there a Grantee by your computer login name? Yes? Skip next line
    - Click +, select Grantee as your computer login name.
    - Set Privileges to all -> save
5 In run.py (line 18), a file 'dbLogin.txt' is referenced. This file should be
  located in the same directory as run.py. It should contain one line
  with the user's (that's you) database credentials.
    - Example: postgresql://postgres:YOUR_PASSWORD@localhost/test
5 Open terminal at awesome-hyperopt folder. Start venv. cd server (where run.py lives).
6 now type as below (in venv)
	(venv)$ python
	>>> from run import db
	>>> db.create_all()
7 View tables in database from the pgadmin4 page:
    - Expand test->Databases->db->Schemas->public->Tables
    - Right click table -> View/Edit Data -> All Rows



# Steps to Run

1 Open terminal at awesome-hyperopt folder
2 Start virtual environment
3 cd server
4 $python run.py
5 Start pgadmin4
6 Open terminal at awesome-hyperopt/client (where package.json lives) and enter
    $npm run dev
7 Open browser and go to http://localhost:8080/


## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# Not implemented, but command will try to run
# run unit tests
npm run unit

# Not implemented, but command will try to run
# run e2e tests
npm run e2e

# Not implemented, but command will try to run
# run all tests
npm test


