docker compose -f .\docker-compose-base-client.yml down && docker compose -f .\docker-compose-base-client.yml up --build --no-start && docker compose -f .\docker-compose-base-client.yml up -d