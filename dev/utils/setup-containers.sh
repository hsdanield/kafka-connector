#!bin/bash

path_server="./debezium-connector-base/docker-compose-base.yml"
path_client="./debezium-connector-base-client/docker-compose-base-client.yml"
compose_cmd="docker compose -f"
down_cmd="down"
up_cmd="up -d"

## Down containers
$compose_cmd $path_server $down_cmd
$compose_cmd $path_client $down_cmd

# Up Containers
$compose_cmd $path_server $up_cmd
sleep 10
$compose_cmd $path_client $up_cmd

