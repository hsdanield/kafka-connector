#!/bin/bash


sudo chmod 666 /var/run/docker.sock


echo "Iniciando Containers Oracle e Postgres"
docker start $(docker ps -a -f name="oracle|postgres" -q)
sleep 3

echo "Build containers"
docker compose -f ./client-connector-base/docker-compose.yml down
docker compose -f ./server-connector-base/docker-compose.yml down
docker compose -f ./server-connector-base/docker-compose.yml up -d --build --no-start
docker compose -f ./client-connector-base/docker-compose.yml up -d --build --no-start
sleep 5

echo "Iniciando Conectores"
docker compose -f ./server-connector-base/docker-compose.yml up -d 
sleep 5
docker compose -f ./client-connector-base/docker-compose.yml up -d
sleep 5

echo "Copiando arquivos de conexao"
docker cp ./client-connector-base/client-connector/connectors_template/ connect-client:/kafka/ 
sleep 8

echo "Arquivo de configuracao signal ORACLE >> cliente1-orclcdb-conn"
docker exec connect-client /bin/bash -c "curl -X PUT -H 'Content-Type:application/json' http://localhost:8083/connectors/cliente1-orclcdb-conn/config -d @/kafka/connectors_template/oracle_signal.json"
sleep 5

echo "Arquivo de configuracao signal SQLSERVER >> cliente1-sqlserver-conn"
docker exec connect-client /bin/bash -c "curl -X PUT -H 'Content-Type:application/json' http://localhost:8083/connectors/cliente1-sqlserver-conn/config -d @/kafka/connectors_template/mssql_signal.json"
sleep 5


echo "


Concluido...
"



