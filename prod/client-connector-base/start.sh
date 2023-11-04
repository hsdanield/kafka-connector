docker compose down && \
docker compose up --build --no-start
docker compose up -d
sleep 10

docker exec connect-client /bin/bash -c "curl -X PUT -H 'Content-Type:application/json' http://localhost:8083/connectors/cliente1-orclcdb-conn/config -d @/kafka/connectors_template/oracle.json"
sleep 5
docker exec connect-client /bin/bash -c "curl -X PUT -H 'Content-Type:application/json' http://localhost:8083/connectors/cliente2-testeDB-conn/config -d @/kafka/connectors_template/mssql.json"
echo "\n"