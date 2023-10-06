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

You can install dependencies using pip or Poetry.

##### Using pip

    pip install -r requirements.txt

##### Using Poetry :

First install poetry :

    pip install poetry

then install dependencies:

    poetry install

#### Flake8 :

Flake8 is not a mandatory dependency, so you must add it manually.

    pip install flake8

then run :

    flake8

## Run the local server :

Go to the softdesk folder :

    cd softdesk

Run the server :

    python manage.py runserver
    
or using poetry :

    poetry run python manage.py runserver

By default the port is 8000, but you can change it, e.g. to use port 8001 instead you can do :

    python manage.py runserver 8001 

⚠️ If you change the port, make sure you also change it in the url, replacing 8000 with the new port.

## Usage :

### The API can be accessed using a variety of tools :
- [Postman](https://www.postman.com/) (recommended)
- [cURL](https://curl.se)
- Using a browser through the Django Rest Framework Browsable API at http://127.0.0.1:8000/api/

  - You must be logged in, as the Authorization header cannot be sent.

    - login url : http://127.0.0.1:8000/api-auth/login/
    - logout url : http://127.0.0.1:8000/api-auth/logout/
  -  Then use urls as described bellow.

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
            <th>Headers</th>
            <th>Data</th>
            <th>Permissions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/users/</code></td>
            <td>Get all users</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td>
                <ul>
                    <li>Admin</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>POST</code></td>
            <td><code>/api/users/</code></td>
            <td>Create an account</td>
            <td></td>
<td>

```json
{
    "username": "username",
    "password": "password",
    "email": "email@exemple.com",
    "birthdate": "YYYY-MM-DD",
    "can_be_contacted": true,
    "can_data_be_shared": true,
}
```
</td>
            <td>
                <ul>
                    <li>Everyone</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/users/{user_id}/</code></td>
            <td>Get a user</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td>
                <ul>
                    <li>Admin</li>
                    <li>Data owner</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>DELETE</code></td>
            <td><code>/api/users/{user_id}/</code></td>
            <td>Delete a user</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td>
                <ul>
                    <li>Admin</li>
                    <li>Data owner</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>PUT</code></td>
            <td><code>/api/users/{user_id}/</code></td>
            <td>Update a user</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
<td>

```json
{
    "username": "username",
    "password": "password",
    "email": "email@exemple.com",
    "birthdate": "YYYY-MM-DD",
    "can_be_contacted": true,
    "can_data_be_shared": true,
}
```
</td>
            <td>
                <ul>
                    <li>Admin</li>
                    <li>Data owner</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>PATCH</code></td>
            <td><code>/api/users/{user_id}/</code></td>
            <td>Partial user update</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
<td>

```json
{
    "username": "username"
}
```
</td>
            <td>
                <ul>
                    <li>Admin</li>
                    <li>Data owner</li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

<br/>

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

```json
{
    "username": "username",
    "password": "password",
}
```
</td>
            <td>
                <ul>
                    <li>Everyone, but requires an account</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>POST</code></td>
            <td><code>/token/refresh/</code></td>
            <td>Refresh JW Token</td>
<td>

```json
{
    "refresh": "{token}"
}
```
</td>
            <td>
                <ul>
                    <li>Everyone, but requires an access token</li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

<br/>

#### Project :

<table>
    <thead>
        <tr>
            <th>Method</th>
            <th>URL</th>
            <th>Description</th>
            <th>Headers</th>
            <th>Data</th>
            <th>Choices</th>
            <th>Permissions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/projects/</code></td>
            <td>Get all projects</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td></td>
            <td>
                <ul>
                    <li>Authenticated user</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>POST</code></td>
            <td><code>/api/projects/</code></td>
            <td>Create a project</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
<td>

```json
{
    "name": "project's name",
    "description": "project's description",
    "type": "BACKEND"
}
```
</td>
<td>

```json
"type": {
    "BACKEND",
    "FRONTEND",
    "iOS",
    "ANDROID",
}
```
</td>
            <td>
                <ul>
                    <li>Authenticated user</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/projects/{project_id}/</code></td>
            <td>Get a project</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td></td>
            <td>
                <ul>
                    <li>Project's contributor</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>DELETE</code></td>
            <td><code>/api/projects/{project_id}/</code></td>
            <td>Delete a project</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td></td>
            <td>
                <ul>
                    <li>Project's author</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>PUT</code></td>
            <td><code>/api/projects/{project_id}/</code></td>
            <td>Update a project</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
<td>

```json
{
    "name": "project's name",
    "description": "project's description",
    "type": "BACKEND"
}
```
</td>
<td>

```json
"type": {
    "BACKEND",
    "FRONTEND",
    "iOS",
    "ANDROID",
}
```
</td>
            <td>
                <ul>
                    <li>Project's author</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>PATCH</code></td>
            <td><code>/api/projects/{project_id}/</code></td>
            <td>Partial project update</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
<td>

```json
{
    "description": "description updated"
}
```
</td>
<td>

```json
"type": {
    "BACKEND",
    "FRONTEND",
    "iOS",
    "ANDROID",
}
```
</td>
            <td>
                <ul>
                    <li>Project's author</li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

<br/>

#### Contributor :

<table>
    <thead>
        <tr>
            <th>Method</th>
            <th>URL</th>
            <th>Description</th>
            <th>Headers</th>
            <th>Data</th>
            <th>Permissions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/projects/{project_id}/contributors/</code></td>
            <td>Get all contributors</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td>
                <ul>
                    <li>Project's contributor</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>POST</code></td>
            <td><code>/api/projects/{project_id}/contributors/</code></td>
            <td>Add a contributor</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
<td>

```json
{
    "user": "username",
}
```
</td>
            <td>
                <ul>
                    <li>Project's author</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/projects/{project_id}/contributors/{contributor_id}/</code></td>
            <td>Get a contributor</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td>
                <ul>
                    <li>Project's contributor</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>DELETE</code></td>
            <td><code>/api/projects/{project_id}/contributors/{contributor_id}/</code></td>
            <td>Delete a contributor</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td>
                <ul>
                    <li>Project's author</li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

<br/>

#### Issue :

<table>
    <thead>
        <tr>
            <th>Method</th>
            <th>URL</th>
            <th>Description</th>
            <th>Headers</th>
            <th>Data</th>
            <th>Choices</th>
            <th>Permissions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/projects/{project_id}/issues/</code></td>
            <td>Get all issues</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td></td>
            <td>
                <ul>
                    <li>Project's contributor</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>POST</code></td>
            <td><code>/api/projects/{project_id}/issues/</code></td>
            <td>Create an issue</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
<td>

```json
{
    "name": "issue's name",
    "description": "issues's description",
    "assigned_to" : "test",
    "priority": "HIGH",
    "tag": "BUG",
    "status": "To Do"
}
```
</td>
<td>

```json
"assigned_to" : {
    "username of a project contributor"
},
"priority": {
    "HIGH",
    "MEDIUM",
    "LOW"
},
"tag": {
    "BUG",
    "FEATURE",
    "TASK"
},
"status" : {
    "To Do",
    "In Progress",
    "Finished"
}
```
</td>
            <td>
                <ul>
                    <li>Project's contributor</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/projects/{project_id}/issues/{issue_id}/</code></td>
            <td>Get an issue</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td></td>
            <td>
                <ul>
                    <li>Project's contributor</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>DELETE</code></td>
            <td><code>/api/projects/{project_id}/issues/{issue_id}/</code></td>
            <td>Delete an issue</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td></td>
            <td>
                <ul>
                    <li>Issue's author</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>PUT</code></td>
            <td><code>/api/projects/{project_id}/issues/{issue_id}/</code></td>
            <td>Update an issue</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
<td>

```json
{
    "name": "issue's name",
    "description": "issues's description",
    "assigned_to" : "test",
    "priority": "HIGH",
    "tag": "BUG",
    "status": "To Do"
}
```
</td>
<td>

```json
"assigned_to" : {
    "username of a project contributor"
},
"priority": {
    "HIGH",
    "MEDIUM",
    "LOW"
},
"tag": {
    "BUG",
    "FEATURE",
    "TASK"
},
"status" : {
    "To Do",
    "In Progress",
    "Finished"
}
```
</td>
            <td>
                <ul>
                    <li>Issue's author</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>PATCH</code></td>
            <td><code>/api/projects/{project_id}/issues/{issue_id}/</code></td>
            <td>Partial issue update</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
<td>

```json
{
    "description": "description updated"
}
```
</td>
<td>

```json
"assigned_to" : {
    "username of a project contributor"
},
"priority": {
    "HIGH",
    "MEDIUM",
    "LOW"
},
"tag": {
    "BUG",
    "FEATURE",
    "TASK"
},
"status" : {
    "To Do",
    "In Progress",
    "Finished"
}
```
</td>
            <td>
                <ul>
                    <li>Issue's author</li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

<br/>

#### Comment :

<table>
    <thead>
        <tr>
            <th>Method</th>
            <th>URL</th>
            <th>Description</th>
            <th>Headers</th>
            <th>Data</th>
            <th>Permissions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/projects/{project_id}/issues/{issue_id}/comments/</code></td>
            <td>Get all comments</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td>
                <ul>
                    <li>Project's contributor</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>POST</code></td>
            <td><code>/api/projects/{project_id}/issues/{issue_id}/comments/</code></td>
            <td>Create a comment</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
<td>

```json
{
    "description": "Comment's description"
}
```
</td>
            <td>
                <ul>
                    <li>Project's contributor</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>GET</code></td>
            <td><code>/api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/</code></td>
            <td>Get a comment</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td>
                <ul>
                    <li>Project's contributor</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>DELETE</code></td>
            <td><code>/api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/</code></td>
            <td>Delete a comment</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
            <td></td>
            <td>
                <ul>
                    <li>Comment's author</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>PUT</code></td>
            <td><code>/api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/</code></td>
            <td>Update a comment</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
<td>

```json
{
    "description": "comment's description"
}
```
</td>
            <td>
                <ul>
                    <li>Comment's author</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td><code>PATCH</code></td>
            <td><code>/api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/</code></td>
            <td>Partial comment update</td>
<td>

```json
{
    "Authorization": "Bearer {token}"
}
```
</td>
<td>

```json
{
    "description": "description updated"
}
```
</td>
            <td>
                <ul>
                    <li>Comment's author</li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>

<br/>

## Contact :
Jonathan Singer - john.t.singer@gmail.com\
Project link : https://github.com/johntsinger/da-python-p10
