## Windows
docker compose -f .\debezium-connector-base\docker-compose-base.yml down --rmi all && docker compose -f .\debezium-connector-base\docker-compose-base.yml up --build --no-start && docker compose -f .\debezium-connector-base\docker-compose-base.yml up -d

## Linux Removendo todas as imagens existentes
docker compose -f ../debezium-connector-base/docker-compose-base.yml down --rmi all && docker compose -f ../debezium-connector-base/docker-compose-base.yml up --build --no-start && docker compose -f ../debezium-connector-base/docker-compose-base.yml up -d && \
docker compose -f ../debezium-connector-base-client/docker-compose-base-client.yml down --rmi all && docker compose -f ../debezium-connector-base-client/docker-compose-base-client.yml up --build --no-start && docker compose -f ../debezium-connector-base-client/docker-compose-base-client.yml up -d 


## Removendo somente containers
docker compose -f ../debezium-connector-base/docker-compose-base.yml down && \
docker compose -f ../debezium-connector-base-client/docker-compose-base-client.yml down && \
docker compose -f ../debezium-connector-base/docker-compose-base.yml up -d && \
docker compose -f ../debezium-connector-base-client/docker-compose-base-client.yml up -d && \
docker cp ../debezium-connector-base-client/debezium-with-oracle-jdbc/connectors_template/ connect-client:/kafka/


## Templates Connector Cliente
docker exec connect-client /bin/bash -c "curl -i -X PUT -H 'Content-Type:application/json' http://localhost:8083/connectors/cliente1-orclcdb-connector/config -d @/kafka/connectors_template/oracle_v4.json" \
&& docker exec connect-client /bin/bash -c "curl -i -X PUT -H 'Content-Type:application/json' http://localhost:8083/connectors/cliente2-testeDB2-connector/config -d @/kafka/connectors_template/mssql_v3.json"