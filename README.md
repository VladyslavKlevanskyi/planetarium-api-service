# Planetarium-api-service
Project for managing API service with the ability to buy tickets and make orders.

# Introduction

The goal of the project is to learn DRF by creating a simple service for making reservations to astronomy shows.


![Default Home View](_screenshots/Main.jpg?raw=true "Index")

### Main features

* The project contains 6 models
![Default Home View](_screenshots/DB_Structure.jpg?raw=true "DB structure")

* User registration and logging are implemented

* JWT authenticated

* Admin panel `/admin/`

* Documentation is located at `/api/doc/swagger/`

* Managing reservations and tickets

* Creating astronomy shows with show themes

* Uploading images for astronomy show

* Creating planetarium domes

* Adding show sessions

* Filtering astronomy shows by title and data

* Filtering show sessions by show time and astronomy shows

* PostgreSQL database

# Setup

### 1. Clone project from GitHub to local computer.

Open the Git Bash console in the directory where you want to place the project. Run command:

    $ git clone https://github.com/VladyslavKlevanskyi/planetarium-api-service.git

### 2. Create virtual environment

Open the project and run command:

    $ python -m venv venv
    
And then activate virtualenv:
    
a) For windows:

    $ venv\Scripts\activate
   
b) For mac:

    $ source venv/bin/activate
      

### 3. Installing project dependencies

Run command:

    $ pip install -r requirements.txt

### 4. Adding a secret key to the project

Generate a new secret key:

    $ python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Rename `.env.sample` file to `.env.docker`. Open it and replace `<your_secret_key>` with the key you generated before.

### 5. Adding Database Settings

In file `.env.docker` enter database name - `POSTGRES_HOST=db`. You can fill in all remaining fields (`POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD`) as you wish.

### 6. Run with docker

Docker should be installed. Run these commands one by one:

    $ docker-compose build
    $ docker-compose up

### 7. Go into a Docker container's shell

To enter in your Docker container's shell, you first need to know `CONTAINER ID`.
Use the command in the terminal:

    $ docker ps

You can see `CONTAINER ID` of you image. To enter inside the container, use command:

    $ docker exec -it XXXXXXXXXXXX bash

Where `XXXXXXXXXXXX` - is `CONTAINER ID` of you image.


### 8. Run tests

In order to make sure that the project is working correctly, run the tests with the command:

    $ python manage.py test 

### 9. Load data into database:

To fill the database, load the `.json` file with the command:
    
    $ python manage.py loaddata planetarium_db.json



### 10. Getting access

To getting access to all resources you need to generate a token. To do this you need to go to:

    http://127.0.0.1:8000/api/user/token/

Enter credentials:
* Email - `admin@admin.admin`
* Password - `1QaZxCdE3`

Now you can use "access" token with **ModHeader** plugin for example.

Go to main page:

    http://127.0.0.1:8000/api/planetarium/

Enjoy!
