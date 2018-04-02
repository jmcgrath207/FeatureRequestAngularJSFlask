
Client Feature Request
==
[![Travis CI Build](https://travis-ci.org/jmcgrath207/Feature-Request-Python-Flask.svg?branch=master)](https://travis-ci.org/jmcgrath207/Feature-Request-Python-Flask) [![Coverage Status](https://coveralls.io/repos/github/jmcgrath207/Feature-Request-Python-Flask/badge.svg?branch=master)](https://coveralls.io/github/jmcgrath207/Feature-Request-Python-Flask?branch=master) [![Code Health](https://landscape.io/github/jmcgrath207/Feature-Request-Python-Flask/master/landscape.svg?style=flat)](https://landscape.io/github/jmcgrath207/Feature-Request-Python-Flask/master)

 
Source Code for the Client Feature Request Project

![Main Image](https://github.com/jmcgrath207/Feature-Request-Python-Flask/raw/master/img/main_pic.png)

## Docker

Build Docker containers with Docker compose

```bash
git clone https://github.com/jmcgrath207/Feature-Request-Python-Flask.git
cd Feature-Request-Python-Flask/
docker-compose build
docker-compose up -d
```

Tear down Docker containers.

```bash
docker-compose down
```

## Configuration

### Linux Environment variables
 
### On Build 
On Build, you can set different variables to allow 

For example, you can disable Root ssh login when you build the Docker image.

```bash
SSH_ROOT_LOGIN=False
```

This is can be found in path ./Feature-Request-Python-Flask/web/app/.start_env

***It is highly suggested that you change your password after build since it will be in the 
Image Layer. This is found in the .start_env file***

### After Build

If you want to change the Flask key, you can find it here

```python
FLASK_SECRET_KEY=replace_me!
```

This is can be found in path ./Feature-Request-Python-Flask/web/app/.after_build_env


### Flask
There is a variable that allows you log in without creating an account named NO_PASSWORD.
By default, it is set to False, which prevents accounts from being made via login.

This can be found in the path /Feature-Request-Python-Flask/web/app/config.py of the project folder.

ex.

```python
NO_PASSWORD = False
```

## API

The client feature project offers a RESTful API

#### Get API KEY

```bash

curl -H "Content-Type: application/json" -X POST -d '{"Client_id":"clientid", "Password":"password"}' \
http://127.0.0.1/api_key


{
  "API KEY": "Ohe0cUSguTTSvqY67MwqYTqqn935HC.Cso2bQ.5BZdfmAaZFz9qaGyTqJSAzXuMYA"
}
```
Note: Each API Key expires after 24 hours

#### POST

Use the API KEY to POST data to the Feature Client Portal.



```bash

curl -H "Content-Type: application/json" -H "API_KEY:<api-key>" -H "Client_ID:<clientid>" \
-X POST -d '{"case_name": "This is a case", "description": "About the Case", "priority": 1, "product_area": "sales", "target_date": "10/21/2017"}' \
http://127.0.0.1/api/client_view


{
  "success": "Data has been successful POST"
}
```

#### GET

To grab case information, follow the example below.

```bash

curl  -H "API_KEY:<api-key>" -H "Client_ID:<clientid>" http://127.0.0.1/api/client_view



[
    {
        "case_name": "sample case",
        "case_number": 7,
        "description": "something",
        "priority": 1,
        "product_area": "Engineering",
        "status": "In Progress",
        "target_date": "10/7/2016"
    },

```
