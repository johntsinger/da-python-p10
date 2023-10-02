# Python Application Developer - P10 - Create a secure RESTful API using Django REST

## Description :

REST Api for front-end applications with a secure backend for projects management.

## Installation guide

### Clone repository with Git :

    git clone https://github.com/johntsinger/da-python-p10.git
    
or

### Download the repository :

- On the [project page](https://github.com/johntsinger/da-python-p10)
- Click on green Code button
- Click on download ZIP
- Extract the file.

### Install Python :

If you don't have Python 3, please visit : https://www.python.org/downloads/ to download it !

### Virtual Environment :

#### Create a virtual environment in the project root :

    python -m venv env

#### Activate a virtual environment :

##### windows :

    env/Scripts/activate
    
##### linux/mac :

    source env/bin/activate
    
#### Install dependencies :

    pip install -r requirements.txt

## Run the local server :

Go to the softdesk folder :

    cd softdesk

Run the server :

    python manage.py runserver

By default the port is 8000, but you can change it, e.g. to use port 8001 instead you can do :

    python manage.py runserver 8001 

⚠️ If you change the port, make sure you also change it in the url, replacing 8000 with the new port.

## Usage :

### The API can be accessed using a variety of tools :
  - [Postman](https://www.postman.com/) (recommended)
  - [cURL](https://curl.se)
  - Using a browser through the Django Rest Framework Browsable API at http://127.0.0.1:8000/api/

### Users :

##### Admin User :

| ID | Username | Password |
| --- | --- | --- |
| 1 | admin | password |

Admin user can access Django admin interface at http://127.0.0.1:8000/admin/

##### Normal User:

| ID | Username | Password |
| --- | --- | --- |
| 2 | test | wxcv1234 |
| 3 | test2 | wxcv1234 |


### Endpoints :

| Category | Description | HTTP method | URL *(base : http://127.0.0.1:8000/api)* |
| :---: | --- | :---: | --- |
| *User* |
| # | Create an account | POST | /users/ |
| # | Get all users *(admin only)* | GET | /users/ |
| # | Get a user *(admin or data owner)* | GET | /users/{id}/ |
| # | Delete a user *(admin or data owner)* | DELETE | /users/{id}/ |
| # | Update a user *(admin or data owner)* | PUT / PATCH | /users/{id}/ |
| *Token* |
| # | Get JW Token *(User registered)* | POST | /token/ |
| # | Refresh JW Token *(User registered)* | POST | /token/refresh |
| *Project* |
| # | Get all projects *(Authenticated user)* | GET | /projects/ |
| # | Create a project *(Authenticated user)* | POST | /projects/ |
| # | Get a project *(contributors only)* | GET | /projects/{id}/ |
| # | Delete a project *(author only)* | DELETE | /project/{id}/ |
| # | Update a project *(author only)* | PUT / PATCH | /project/{id}/ |
| *Contributor*|
| # | Get all contributors *(contributors only)* | GET | /projects/{id}/contributors/ |
| # | Add a contributor *(author only)* | POST | /projects/{id}/contributors/ |
| # | Get a contributor *(contributors only)* | GET | /projects/{id}/contributors/{id}/ |
| # | Remove a contributor *(author only)* | DELETE | /project/{id}/contributors/{id}/ |
| *Issue* |
| # | Get all issues *(contributors only)* | GET | /projects/{id}/issues/ |
| # | Create an issue *(contributors only)* | POST | /projects/{id}/issues/ |
| # | Get an issue *(contributors only)* | GET | /projects/{id}/issues/{id}/ |
| # | Delete an issue *(issue's author or project's author)* | DELETE | /project/{id}/issues/{id}/ |
| # | Update an issue *(issue's author or project's author)* | PUT / PATCH | /project/{id}/issues/{id}/ |
| *Comment*|
| # | Get all comments *(contributors only)* | GET | /projects/{id}/issues/{id}/comments/ |
| # | Create a comments *(contributors only)* | POST | /projects/{id}/issues/{id}/comments/ |
| # | Get a comment *(contributors only)* | GET | /projects/{id}/issues/{id}/comments/{id}/ |
| # | Delete a comment *(comment's author or project's author)* | DELETE | /project/{id}/issues/{id}/comments/{id}/ |
| # | Update a comment *(comment's author or project's author)* | PUT / PATCH | /project/{id}/issues/{id}/comments/{id}/ |

## Contact :
Jonathan Singer - john.t.singer@gmail.com\
Project link : https://github.com/johntsinger/da-python-p10
