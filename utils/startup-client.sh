docker compose -f .\debezium-connector-base-client\docker-compose-base-client.yml down --rmi all && docker compose -f .\debezium-connector-base-client\docker-compose-base-client.yml up --build --no-start && docker compose -f .\debezium-connector-base-client\docker-compose-base-client.yml up -d 


docker compose -f ./debezium-connector-base-client/docker-compose-base-client.yml down --rmi all && docker compose -f ./debezium-connector-base-client/docker-compose-base-client.yml up --build --no-start && docker compose -f ./debezium-connector-base-client/docker-compose-base-client.yml up -d 