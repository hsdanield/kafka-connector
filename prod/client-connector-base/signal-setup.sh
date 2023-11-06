echo "Copiando arquivos de conexao"
docker cp ./client-connector/connectors_template/ connect-client:/kafka/ 
sleep 8

echo "Arquivo de configuracao signal >> cliente1-orclcdb-conn"
docker exec connect-client /bin/bash -c "curl -X PUT -H 'Content-Type:application/json' http://localhost:8083/connectors/cliente1-orclcdb-conn/config -d @/kafka/connectors_template/oracle_signal.json"

echo "Agora Rodar o Insert na tabela debezium_signal"