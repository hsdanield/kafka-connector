docker cp ../debezium-connector-base-client/debezium-with-oracle-jdbc/connectors_template/ connect-client:/kafka/
docker exec connect-client /bin/bash -c "curl -i -X PUT -H 'Content-Type:application/json' http://localhost:8083/connectors/cliente2-testDB2-connector/config -d @/kafka/connectors_template/mssql_v3.json"