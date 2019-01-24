# Functional requirements
* Users are able to submit reviews to the API
* Users are able to retrieve reviews that they submitted
* Users cannot see reviews submitted by other users
* Use of the API requires a unique auth token for each user
* Submitted reviews must include, at least, the following attributes:
* Rating - must be between 1 - 5
* Title - no more than 64 chars
* Summary - no more than 10k chars
* IP Address - IP of the review submitter
* Submission date - the date the review was submitted
* Company - information about the company for which the review was submitted, can be simple text (e.g., name, company id, etc.) or a separate model altogether
* Reviewer Metadata - information about the reviewer, can be simple text (e.g., name, email, reviewer id, etc.) or a separate model altogether

# Overview

The project can be run on bare bone, docker and virtenv

# Docker

Visit https://www.docker.com/products/docker-desktop to download and install it

### Build
The script `cli.sh` is able to build a `docker` image out of the current project files on your drive
E.g. `./cli.sh build` - this will build a docker image based on `python:3-alpine` and tag it as `reviews`
This phase automatically install all dependencies, run DB migrations and run the tests. So, you don't need to do anything else. For local setup, please read below.


### Running locally

There are two modes of running the app
* Normal mode: Run within "encapsulated" docker container, i.e. whatever changes you make in your DB, once you stop the container, it's gone. The project/source files are only visible in the container and they can be changed only if you ssh to it
* Locally (dev) mode: Run a docker container with mounted `pwd`. The project files from your disk are mounted and used by the docker container. Sqlite3 DB is also created there, so your changes will be saved. You can stop and run the container safely

#### Just want to run it - use the `Normal` mode
There is a `docker` integration, so the application can be very easy run locally by simply installing Docker and then using the system script `cli.sh` which is self-explained.
E.g. `./cli.sh build-and-run`. You can ship the docker image to everyone, or in some docker repo and everyone can run it by calling `./cli.sh run`

#### Run and develop - `Local` mode with `Docker`
*First time you run it in dev mode - run `./cli.sh manage.py migrate` to create the DB*

Call `./cli.sh build-and-run-locally` which uses the python code from the `pwd` (currently working dir) instead of the in-image one
Note: When you run the docker container "locally", i.e. mounting host directory, the host dir should contain the whole project `reviews`. The `build` step will create `db.sqlite3` file - the DB `INSIDE` the container, so you need to run `./cli.sh manage.py migrate` if you haven't in order to create the DB locally

### manage.py
Once you build & run it, you could create a super user for django admin, or run migrations, etc. by running `./cli.sh manage.py <command>`

NB: If you run that command in `locally` setup, i.e. after `./cli.sh run-locally` or `./cli.sh build-and-run-locally` the changes of the command will affect the `pwd` folder you already mounted by running the app locally

Warning: if you see an error like `Error: No such container: bash` it means that the container is not running, please run `./cli.sh run` or `./cli.sh run-locally` first

### test
`/cli.sh test` is a shortcut to run the django tests against a running container. Anyway, they are automatically run on every build

### exec
You can easily ssh to the container or just execute a command there by simply `./cli.sh exec <command>`

### Creating superuser
`./cli.sh manage.py createsuperuser`

# Virtualenv

### Command line
* First you have to install python3
* ./cli.sh virtenv-create (only the first time)
* ./cli.sh virtenv-run (every time you want to run it)
If you want to run oher commands: `source ./vert/bin/activae` and enjoy

### PyCharm
* VCS -> Checkout from Version Control -> Git -> https://github.com/vzelev/reviews.git
* ./cli.sh virtenv-create
* Preferences -> Project reviews -> project interpreter -> show all -> the `+` button -> choose the one inside the project

# API docs
Open `http://localhost:8000/`
Swagger uses Session authentication to call the endpoints due to it's limits. Please note that the protected endpoints, i.e. `/api/v1/reviews/` are not visible in Swagger if there is no active Session, so please use the `Session Login` button to login and the you will be able to see and call them.

![Screenshot](docs/swagger_not_auth.png)

And now...

![Screenshot](docs/swagger_auth.png)

# User registration

User registration is handled by `/api/v1/api-auth/register/` endpoint. Please, refer to the `/` (docs) endpoint for more information

# API Token obtaining

Once the user has been registered successfully, he/she could obtain a token using the `/api/v1/api-auth/obtain-api-token/` endpoint. Please, refer to the `/` (docs) endpoint for more information

# Admin

Django admin is fully functional, it can be accessed on `/admin` page.

# CURL Examples

```
curl --request GET \
  --url http://localhost:8000/api/v1/reviews/ \
  --header 'Accept: application/json' \
  --header 'Authorization: Token SOMETOKEN' \
  --header 'Content-Type: application/json' \
  --header 'Postman-Token: f43ddbd5-39fb-4f57-a68a-d620085b401a' \
  --header 'cache-control: no-cache'
```

```
curl --request POST \
  --url http://localhost:8000/api/v1/reviews/ \
  --header 'Accept: application/json' \
  --header 'Authorization: Token da56cff9606ec06cb32068366dc4da108653813a' \
  --header 'Content-Type: application/json' \
  --header 'Postman-Token: 51ac2438-4f3a-4161-a6da-b608a074143a' \
  --header 'cache-control: no-cache' \
  --data '{\n	"rating": 2,\n	"title": "a2bs",\n	"summary": "hsdsdsdaaa",\n	"company": "lisgnla",\n	"reviewer": "asdsdsdsdz"\n}'
```