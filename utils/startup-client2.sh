
# Atualizar Conector
docker cp ./debezium-connector-base-client/debezium-with-oracle-jdbc/connectors_template/ connect-client:/kafka/

# Cadastro Connector
docker exec connect-client /bin/bash -c "curl -i -X PUT -H 'Content-Type:application/json' http://localhost:8083/connectors/cliente1-orclcdb-connector/config -d @/kafka/connectors_template/oracle_v3.json"

# Cadastro Connector 2
docker exec connect-client /bin/bash -c "curl -i -X POST -H 'Content-Type:application/json' http://localhost:8083/connectors -d @/kafka/connectors_template/oracle_v2.json"

# Restart connector
docker exec connect-client /bin/bash -c "curl -s -X POST http://localhost:8083/connectors/cliente1-orclcdb-connector/restart"



## Criar sinks
cd code && python .\automatizacao_connector.py && cd ..

## Teste tables
cd code && python .\teste_carga_source.py && cd ..