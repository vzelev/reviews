#!/usr/bin/env bash

case "$1" in
    "help"|"")
        cat << EOF
Usage: $0 command [parameters]
    build|b
        Build docker image
    run|r
        run the application on port 8000
    run-locally|rl
        run the application on port 8000 mounting the pwd as a docker working dir
    build-and-run|br
       build docker image and run it
    build-and-run-locally|brl
       build docker image and run it mounting the pwd as a docker working dir
EOF
        ;;
    "b"|"build")
        docker build -t reviews . || exit 1
        ;;
     "r"|"run")
        docker run -p 8000:8000 reviews
        ;;
     "rl"|"run-locally")
        echo "Running..."
        docker run -v `pwd`:/app -p 8000:8000 reviews
        ;;
      "build-and-run"|"br")
        $0 b
        $0 r
        ;;
      "build-and-run-locally"|"brl")
        $0 b
        $0 rl
        ;;
      "manage.py")
        docker exec -it `docker ps | grep reviews | cut -d " " -f 1` bash -c "python /app/manage.py $2"
        ;;
esac