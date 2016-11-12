
#Client Feature Request
==
[![Travis CI Build](https://travis-ci.org/sonance207/Feature-Request-Python-Flask.svg?branch=master)](https://travis-ci.org/sonance207/Feature-Request-Python-Flask) [![Codecov Code Coverage](https://codecov.io/gh/sonance207/Feature-Request-Python-Flask/branch/master/graph/badge.svg)](https://codecov.io/gh/sonance207/Feature-Request-Python-Flask) [![Code Health](https://landscape.io/github/sonance207/Feature-Request-Python-Flask/master/landscape.svg?style=flat)](https://landscape.io/github/sonance207/Feature-Request-Python-Flask/master)



 
Source Code for the Client Feature Request Project

##Docker

Build docker containers with docker compose

```bash
git clone https://github.com/sonance207/Feature-Request-Python-Flask.git
cd Feature-Request-Python-Flask/
docker-compose build
docker-compose up -d
```

Tear down Docker containers.

```bash
docker-compose down
```

##Configuration

###Linux Environment variables
 
###On Build 
On Build you can set different variables to allow 

For example you can disable Root ssh login when you build the docker image.

```bash
SSH_ROOT_LOGIN=False
```

This is can be found in path ./Feature-Request-Python-Flask/web/app/.start_env

**It is highly suggested to change your password after build since it will be in the 
Image Layer ex. .start_env file**

###After Build

If you want to change the Flask key you can find it here

```python
FLASK_SECRET_KEY=replace_me!
```

This is can be found in path ./Feature-Request-Python-Flask/web/app/.after_build_env


###Flask
There is a variable that allows you login without creating a account named NO_PASSWORD.
By default it is set to False, which will prevent accounts being made via login.

This is can be found in path /Feature-Request-Python-Flask/web/app/config.py

ex.

```python
NO_PASSWORD = False
```

##API

The client feature project offers a RESTful API

####Get API KEY

```bash

curl -H "Content-Type: application/json" -X POST -d '{"Client_id":"clientid", "Password":"password"}' \
http://127.0.0.1/api_key


{
  "API KEY": "Ohe0cUSguTTSvqY67MwqYTqqn935HC.Cso2bQ.5BZdfmAaZFz9qaGyTqJSAzXuMYA"
}
```
Note: Each API Key will expire in 24 hours, you will have to request
for a new one.

####POST

From here you will use the API KEY to POST data to the Feature Client Portal.



```bash

curl -H "Content-Type: application/json" -H "API_KEY:<api-key>" -H "Client_ID:<clientid>" \
-X POST -d '{"case_name": "This is a case", "description": "About the Case", "priority": 1, "product_area": "sales", "target_date": "10/21/2017"}' \
http://127.0.0.1/api/client_view


{
  "success": "Data has been successful POST"
}
```

####GET

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
