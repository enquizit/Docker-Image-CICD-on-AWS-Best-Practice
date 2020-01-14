#!/bin/bash

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_tag="$dir_here"
tag_name="$( basename $dir_tag)"
dir_repo="$( dirname $dir_tag)"
repo_name="$( basename $dir_repo)"
container_name="${repo_name}-${tag_name}-test"

local_port="80"
container_port="12345"

docker run --rm -dt --name "${container_name}" -p $local_port:$container_port "${repo_name}:${tag_name}" "${container_port}"
sleep 2 # sleep 2 seconds wait web server become ready
curl "http://localhost:${local_port}"
docker container stop "${container_name}"

curl_exit_status=$?
if [ $curl_exit_status != 0 ]
then
    exit $curl_exit_status
fi
