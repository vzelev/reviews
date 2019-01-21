# Please, consider that this is a POC, it is not prod ready yet!

# Build
The script `cli.sh` is able to build a `docker` image out of the current project files on your drive
* `./cli.sh build|b` - this will build a docker image based on `python:3` and tag it as `reviews`

# Running locally

## Just want to run it?
There is a `docker` integration, so the application can be very easy run locally by simply installing Docker and then using the system script `cli.sh` which is self-explained.
E.g. `./cli.sh br` will `build & run` it. You can ship the docker image to everyone, or in some docker repo and everyone can run it by calling `./cli.sh r`

## Run and develop
For developing purposes you can either run it using virtualenv, local python3 (if you have such) or again `docker`.
Call `./build-and-run-locally brl|build-run-locally` which will use the python code from the `pwd` (currently working dir) instead of the built-in one

Note: When you run the docker container "locally", i.e. mounting host directory, the host dir should contain the whole project `reviews`. The `build` step will create `db.sqlite3` file - the DB
NB: The Django dev server is auto-restarting on every code modification


## manage.py
Once you build & run it, you could create a super user for django admin, or run migrations, etc. by running `./cli.sh manage.py <command>`

NB: If you run that command in `locally` setup, i.e. after `cli.sh rl|brl` the changes of the command will affect the `pwd` folder you already mounted by running the app locally

Warning: if you see an error like `Error: No such container: bash` it means that the container is not running, please run `./cli.sh r|br|rl|brl` first