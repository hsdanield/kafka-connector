
# Atualizar Conector
docker cp ./debezium-connector-base-client/debezium-with-oracle-jdbc/connectors_template/ connect-client:/kafka/

# Cadastro Connector
docker exec connect-client /bin/bash -c "curl -i -X PUT -H 'Content-Type:application/json' http://localhost:8083/connectors/cliente1-orclcdb-connector/config -d @/kafka/connectors_template/oracle_v3.json"

# Restart connector
docker exec connect-client /bin/bash -c "curl -s -X POST http://localhost:8083/connectors/cliente1-orclcdb-connector/restart"



## Criar sinks
cd code && python .\automatizacao_connector.py && cd ..