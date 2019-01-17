#!/usr/bin/env bash

case "$1" in
    "help"|"")
        cat << EOF
Usage: $0 command [parameters]
    build|b
        Build docker image
    run|r
        run the application on port 8000 if exists else build it and run it then
    build-and-run|br
       build docker image and run it
EOF
        ;;
    "b"|"build")
        docker build -t reviews .
        ;;
     "r"|"run")
        (docker image ls reviews && docker run -p 8000:8000 reviews) ||
        (docker build -t reveiws . && docker run -p 8000:8000 reviews)
        ;;
      "build-and-run"|"br")
        docker build -t reveiws . || exit 1
        echo "Running..."
        docker run -p 8000:8000 reviews
        ;;
esac