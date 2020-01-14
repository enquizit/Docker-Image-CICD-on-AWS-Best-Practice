#!/bin/bash

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_tag="$dir_here"
tag_name="$( basename $dir_tag)"
dir_repo="$( dirname $dir_tag)"
repo_name="$( basename $dir_repo)"
container_name="${repo_name}-${tag_name}-test"

docker run --rm -dt --name "${container_name}" "${repo_name}:${tag_name}"
sleep 2 # sleep 2 seconds wait web server become ready

check_exit_status() {
    exit_status=$1
    if [ $exit_status != 0 ]
    then
        echo "FAILED!"
        docker container stop "${container_name}"
        exit $exit_status
    fi
}

echo "is requests installed?"
docker exec -t "${container_name}" pip list | grep requests
check_exit_status $?

echo "is beautifulsoup4 installed?"
docker exec -t "${container_name}" pip list | grep beautifulsoup4
check_exit_status $?

docker container stop "${container_name}"
