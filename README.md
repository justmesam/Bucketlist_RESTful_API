[![Build Status](https://travis-ci.org/justmesam/Bucketlist_RESTful_API.svg?branch=master)](https://travis-ci.org/justmesam/Bucketlist_RESTful_API)
[![Coverage Status](https://coveralls.io/repos/github/justmesam/Bucketlist_RESTful_API/badge.svg?branch=heroku-deploy)](https://coveralls.io/github/justmesam/Bucketlist_RESTful_API?branch=heroku-deploy)
# Bucketlist RESTful API

A RESTful API that lets you register, login, logout and reset password for users,   
 create, read, update and delete a bucketlist and/or its items.   


#### Prerequisites:

[Flask][1] : Flask is a microframework for Python  
[Postgres][2] : An open source SQL database   


### API Resource(ENDPOINTS):

## GET:

Endpoint | Function
--------- | ----------
/bucketlists/ | List all bucketlists
/bucketlists/>id</| List a single bucketlists
/bucketlists/>id</items/ | List all items of a specific bucketlist
/bucketlists/>id< /items/ >item_id</ | List a single item
/search/ | List all bucketlists found using a parameter search

## POST:

Endpoint | Function
--------- | ---------
/auth/register/ | Register a user
/auth/login/ | Login a user
/auth/logout/ | Logout a user
/bucketlists/ | Create a bucketlist
/bucketlists/>id</items/ | Create a bucketlist item

## PUT & DELETE:

Endpoint | Function
--------- | ----------
/bucketlists/>id< | Update/Delete an existing bucketlists
/bucketlists/>id< /items/>item_id< | Update/Delete an existing bucketlist item


### Installation

To get your build running just simply do:

* Git clone the repo to your machine;
  >  * git clone https://github.com/justmesam/Bucketlist_RESTful_API.git
  >  * cd Bucketlist_RESTful_API

* Install virtualenv and autoenv globally but if you got them you can skip this step;
> * pip install virtualenv autoenv

* Create a virtualenv and an .env file to store the environment variables;
    * virtualenv ;
        > *  virtualenv venv            

    * .env should have ;
        > source venv/bin/activate  
        export FLASK_APP="run.py"  
        export SECRET_KEY="\x86\x99\x13Q\xd3\xb56d\xb4rfe3\xb2\x06U\x1b\xe2"
        export APP_SETTINGS="config.DevelopmentConfig"  
        export DATABASE_URL="postgresql://localhost/test_api"    

         to activate the environment variables;  `source .env`
* Create a database and do the migrations ;   
    * create database;
      > * createdb test_api
    * to do migrations;  
       * `python manage.py db init`  
       * `python manage.py db migrate`
       * `python manage.py db upgrade`



* Install the requirements;
   > pip install -r requirements.txt

##### Run It!

To start the server just do;
> ./run.py

The server will be running on    `http://127.0.0.1:5000/`   
Now you can include an endpoint of choice;   
eg:   `http://127.0.0.1:5000/auth/register`


You can test on postman or use curl.

[1]: [http://flask.pocoo.org/]
[2]: [https://www.postgresql.org/]
