# RestAPI example project with FastAPI

## How to use
* install the necessary package / dependecies e.g fastapi sqlmodel etc

- with uv
```bash
	$ cd book-api
	$ uv sync
```
-with pip
```bash using pip
	$ cd book-api
	$ python -m venv .venv
	$ source .venv/bin/activate
	$ pip install -r requirement.txt
```
* Copy the env_example to a new .env file
```bash
	$ cp env_example .env
```
* Fill up the the .env file with the required values
* Run fastapi dev server
```bash
	$ fastapi dev
```
	or with uv
```bash
	$ uv run fastapi dev
```

## Auto generated openapi docs
The API comes with the auto generate docs thanks to the great feature from fastapi itself, which can be access via localhost:8000/docs,
<img width="3252" height="1486" alt="image" src="https://github.com/user-attachments/assets/da9c9aab-17d4-4f5b-8dd0-709a7512c598" />

## Endpoint authorization
Some endpoint is accesible only to admin user and can be access via authorization button on the openapi page, use the admin credential that was setup on .env files (e.g. admin email & password) 


