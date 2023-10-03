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

Base URL : http://127.0.0.1:8000/

Prefix : Each url is prefixed with `/api/`

#### User :

<table>
    <thead>
        <tr>
            <th>Method</th>
            <th>URL</th>
            <th>Description</th>
            <th>Data</th>
            <th>Permissions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/users/</code></td>
            <td>Get all users</td>
            <td></td>
            <td>Admin</td>
        </tr>
        <tr>
            <td><code>POST</code></td>
            <td><code>/api/users/</code></td>
            <td>Create an account</td>
<td>
All fields are required

```json
{
    "username": "username",
    "password": "password",
    "email": "email@exemple.com",
    "birthdate": "YYYY-MM-DD",
    "can_be_contacted": true,
    "can_data_be_shared":true,
}
```
</td>
            <td>Everyone</td>
        </tr>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/users/{user_id}/</code></td>
            <td>Get a user</td>
            <td></td>
            <td>Admin</td>
        </tr>
        <tr>
            <td><code>DELETE</code></td>
            <td><code>/api/users/{user_id}/</code></td>
            <td>Delete a user</td>
            <td></td>
            <td>Admin</td>
        </tr>
        <tr>
            <td><code>PUT</code></td>
            <td><code>/api/users/{user_id}/</code></td>
            <td>Update a user</td>
<td>
All fields are required

```json
{
    "username": "username",
    "password": "password",
    "email": "email@exemple.com",
    "birthdate": "YYYY-MM-DD",
    "can_be_contacted": true,
    "can_data_be_shared":true,
}
```
</td>
            <td>Admin<br/>Data owner</td>
        </tr>
        <tr>
            <td><code>PATCH</code></td>
            <td><code>/api/users/{user_id}/</code></td>
            <td>Partial user update</td>
<td>
Only the fields to be updated are required

```json
{
    "username": "username"
}
```
</td>
            <td>Admin<br/>Data owner</td>
        </tr>
    </tbody>
</table>

| HTTP method | URL | Description | Data |
| --- | --- | --- | --- |
| `GET` | `/api/users/` | Get all users *(admin only)* |
| `POST` | `/api/users/` | Create an account | 
| `GET` | `/api/users/{user_id}/` | Get a user *(admin or data owner)* |
| `DELETE` | `/api/users/{user_id}/` | Delete a user *(admin or data owner)* |
| `PUT` | `/api/users/{user_id}/` | Update a user *(admin or data owner)* |
| `PATCH` | `/api/users/{user_id}/` | Update a user *(admin or data owner)* |

#### JW Token :

<table>
    <thead>
        <tr>
            <th>Method</th>
            <th>URL</th>
            <th>Description</th>
            <th>Data</th>
            <th>Permissions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>POST</code></td>
            <td><code>/token/</code></td>
            <td>Claim JW Token</td>
<td>
All fields are required

```json
{
    "username": "username",
    "password": "password",
}
```
</td>
            <td>Registered user</td>
        </tr>
        <tr>
            <td><code>POST</code></td>
            <td><code>/token/refresh</code></td>
            <td>Refresh JW Token</td>
<td>
All fields are required

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```
</td>
            <td>Everyone</td>
        </tr>
    </tbody>
</table>

| HTTP method | URL | Description |
| --- | --- | --- |
| `POST` | `/token/` | Get JW Token *(User registered)* |
| `POST` | `/token/refresh` | Refresh JW Token *(User registered)* |

#### Project :

<table>
    <thead>
        <tr>
            <th>Method</th>
            <th>URL</th>
            <th>Description</th>
            <th>Data</th>
            <th>Permissions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/projects/</code></td>
            <td>Get all projects</td>
            <td></td>
            <td>Authenticated user</td>
        </tr>
        <tr>
            <td><code>POST</code></td>
            <td><code>/api/projects/</code></td>
            <td>Create a project</td>
<td>
All fields are required

type choices : BACKEND, FRONTEND, iOS, ANDROID

```json
{
    "name": "project's name",
    "description": "project's description",
    "type": "BACKEND"
}
```
</td>
            <td>Authenticated user</td>
        </tr>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/projects/{project_id}/</code></td>
            <td>Get a project</td>
            <td></td>
            <td>Contributor</td>
        </tr>
        <tr>
            <td><code>DELETE</code></td>
            <td><code>/api/projects/{project_id}/</code></td>
            <td>Delete a projects</td>
            <td></td>
            <td>Project's author</td>
        </tr>
        <tr>
            <td><code>PUT</code></td>
            <td><code>/api/projects/{project_id}/</code></td>
            <td>Update a project</td>
<td>
All fields are required

type choices : BACKEND, FRONTEND, iOS, ANDROID

```json
{
    "name": "project's name",
    "description": "project's description",
    "type": "BACKEND"
}
```
</td>
            <td>Project's author</td>
        </tr>
        <tr>
            <td><code>PATCH</code></td>
            <td><code>/api/projects/{project_id}/</code></td>
            <td>Partial project update</td>
<td>
Only the fields to be updated are required

```json
{
    "description": "description updated"
}
```
</td>
            <td>Admin<br/>Project's author</td>
        </tr>
    </tbody>
</table>


| HTTP method | URL | Description |
| --- | --- | --- |
| `GET` | `/api/projects/` | Get all projects *(Authenticated user)* |
| `POST` | `/api/projects/` | Create a project *(Authenticated user)* |
| `GET` | `/api/projects/{project_id}/` | Get a project *(contributors only)* |
| `DELETE` | `/api/projects/{project_id}/` | Delete a project *(author only)* |
| `PUT` | `/api/projects/{project_id}/` | Update a project *(author only)* |
| `PATCH` | `/api/projects/{project_id}/` | Update a project *(author only)* |

#### Contributor :

| HTTP method | URL | Description |
| --- | --- | --- |
| `GET` | `/api/projects/{project_id}/contributors/` | Get all contributors *(contributors only)* |
| `POST` | `/api/projects/{project_id}/contributors/` | Add a contributor *(author only)* |
| `GET` | `/api/projects/{project_id}/contributors/{contributor_id}/` | Get a contributor *(contributors only)* |
| `DELETE` | `/api/projects/{project_id}/contributors/{contributor_id}/` | Remove a contributor *(author only)* |

#### Issue :

| HTTP method | URL | Description |
| --- | --- | --- |
| `GET` | `/projects/{project_id}/issues/` | Get all issues *(contributors only)* |
| `POST` | `/projects/{project_id}/issues/` | Create an issue *(contributors only)* |
| `GET` | `/projects/{project_id}/issues/{issue_id}/` | Get an issue *(contributors only)* |
| `DELETE` | `/projects/{project_id}/issues/{issue_id}/` | Delete an issue *(issue's author or project's author)* |
| `PUT` | `/projects/{project_id}/issues/{issue_id}/` | Update an issue *(issue's author or project's author)* |
| `PATCH` | `/projects/{project_id}/issues/{issue_id}/` | Update an issue *(issue's author or project's author)* |

#### Comment :

| HTTP method | URL | Description |
| --- | --- | --- |
| `GET` | `/projects/{project_id}/issues/{issue_id}/comments/` | Get all comments *(contributors only)* |
| `POST` | `/projects/{project_id}/issues/issue_id}/comments/` | Create a comments *(contributors only)* |
| `GET` | /projects/{project_id}/issues/{issue_id}/comments/{comment_id}/ | Get a comment *(contributors only)* |
| `DELETE` | /projects/{project_id}/issues/{issue_id}/comments/{comment_id}/ | Delete a comment *(comment's author or project's author)* |
| `PUT` | `/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/` | Update a comment *(comment's author or project's author)* |
| `PATCH` | `/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/` | Update a comment *(comment's author or project's author)* |

## Contact :
Jonathan Singer - john.t.singer@gmail.com\
Project link : https://github.com/johntsinger/da-python-p10
