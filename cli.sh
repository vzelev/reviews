#!/usr/bin/env bash

case "$1" in
    "help"|"")
        cat << EOF
Usage: $0 command [parameters]
    build
        Build docker image
    run
        run the application on port 8000
    run-locally
        run the application on port 8000 mounting the pwd as a docker working dir
    build-and-run
       build docker image and run it
    build-and-run-locally
       build docker image and run it mounting the pwd as a docker working dir
    manage.py <command>
       Run django <command> against manage.py
    exec <command>
       Run <command> inside the container. It can be whatever you want
    test
       Run Django tests
     virtenv-create
       Create virtual env and prepare the data and run the tests
     virtenv-run
       Run the server
EOF
        ;;
    "build")
        docker build -t reviews . || exit 1
        ;;
     "run")
        echo "Running on localhost:8000"
        docker run --network host reviews
        ;;
     "run-locally")
        echo "Running on localhost:8000"
        docker run -v `pwd`:/app reviews
        ;;
      "build-and-run")
        $0 build
        $0 run
        ;;
      "build-and-run-locally")
        $0 build
        echo Build was successfull. Running...
        echo "PLEASE, IF YOU HAVEN'T RUN ./cli.sh manage.py migrate, run it in separate tab now!"
        $0 run-locally
        ;;
      "manage.py")
        $0 exec "python /app/manage.py $2"
        ;;
       "test")
        $0 manage.py test
        ;;
      "exec")
        docker exec -it `docker ps | grep reviews | cut -d " " -f 1` sh -c "$2"
        ;;
       "virtenv-create")
         pip3 install virtualenv
         virtualenv ./venv -p `which python3`
         source ./venv/bin/activate
         python3 -m pip install -r requirements.txt
         python3 manage.py migrate
         python3 manage.py test
         deactivate
         ;;
        "virtenv-run")
         source ./venv/bin/activate
         ./venv/bin/python3 manage.py runserver
         ;;

esac
