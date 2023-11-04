from confluent_kafka.admin import AdminClient, ConfigResource
from confluent_kafka import Consumer, KafkaError
import json
import re
from pathlib import Path
import yaml
import requests
import sys
import argparse
from pprint import pprint


def loader_yaml(path: str):
    """Rertorna o conteudo de um arquivo yaml"""
    if Path(path).exists():
        with open(Path(path), "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return data
    else:
        print("Arquivo não existente no caminho: ", path)

    return None


class Settings:
    def __init__(
        self,
        path: str = None,
        broker: str = None,
        prefix: str = None,
        kafka_connect_url: str = None,
    ) -> None:
        self.path = path
        self.broker = broker
        self.settings_file = None if self.path is None else loader_yaml(self.path)
        if self.settings_file:
            self.client_prefix = (
                prefix
                if prefix is not None
                else self.settings_file["settings"]["client_prefix"]
            )
            self.kafka_connect_url = self.settings_file["settings"]["kafka_connect_url"]

            self.path_template = self.settings_file["settings"]["path_template"]
            self.datasource = {
                "jdbc_url": self.settings_file["settings"]["datasource"]["jdbc_url"],
                "user": self.settings_file["settings"]["datasource"]["user"],
                "password": self.settings_file["settings"]["datasource"]["password"],
                "tables-map": {
                    table["table"]: {"pks": table["pks"]}
                    for table in self.settings_file["settings"]["datasource"][
                        "tables-map"
                    ]
                },
            }
        if self.broker:
            self.admin_client = AdminClient({"bootstrap.servers": self.broker})

    def __read_sink_template(self, path_template):
        if Path(path_template).exists():
            with open(path_template, "r") as file:
                data = json.load(file)
                return data
        else:
            print("Arquivo não existente no caminho: ", self.path_template)

    def __format_sink_templates(self, path_template, match_topics):
        templates = []
        for t in match_topics.keys():
            template = self.__read_sink_template(path_template)
            template["config"]["topics"] = match_topics[t]["topic"]
            template["config"]["connection.url"] = self.datasource["jdbc_url"]
            template["config"]["connection.username"] = self.datasource["user"]
            template["config"]["connection.password"] = self.datasource["password"]
            template["config"]["table.name.format"] = t
            template["config"]["primary.key.fields"] = ", ".join(match_topics[t]["pks"])
            template["name"] = match_topics[t]["topic"] + "-sink"
            templates.append(template)

        return templates

    def __format_match_map_topic(self, topic_names):
        pattern = r"\.([^\.]+)$"
        tables = self.datasource["tables-map"].keys()
        tables_map = self.datasource["tables-map"]

        for topic in topic_names:
            match = re.search(pattern, topic)
            if match:
                if match.group(1) in tables:
                    tables_map[match.group(1)]["topic"] = topic
            else:
                print("No match topic; " + topic)

        return tables_map

    def list_topics_by_prefix(self, prefix):
        """Lista os topicos do Broker de acordo com o prefixo, e um objeto de mapemaneto de acordo com os topicos encontrados

        Args:
            prefix (str): prefixo para procurar nos topicos

        Returns:
            list[dict{table: <name_of_table>, topic: name_of_topic}]: retorna uma lista de dicionarios com esse mapeamento de tabela e topico
        """

        topic_metadata = self.admin_client.list_topics()
        matching_topics = [
            topic for topic in topic_metadata.topics if topic.startswith(prefix)
        ]

        return matching_topics

    def delete_connectors(self):
        # curl -X DELETE http://<KAFKA_CONNECT_HOST>:<KAFKA_CONNECT_PORT>/connectors/<CONNECTOR_NAME>
        ...

    def consumer_topic(self):
        ...

    def create_sink_connectors(self):
        # Define the headers for the HTTP request
        headers = {"Content-Type": "application/json"}

        topics = self.list_topics_by_prefix(self.client_prefix)
        match_topics = self.__format_match_map_topic(topics)

        print("match topics: ")
        for i, m in enumerate(match_topics):
            print(
                "{i} - topic: {m} || table: {t}".format(
                    i=i, m=match_topics[m]["topic"], t=m
                )
            )

        sink_templates = self.__format_sink_templates(
            path_template=self.path_template, match_topics=match_topics
        )

        for template in sink_templates:
            json_template = json.dumps(template)

            # Send a POST request to create the Kafka Connector
            response = requests.post(
                f"{self.kafka_connect_url}/connectors",
                data=json_template,
                headers=headers,
            )

            # Check the response
            if response.status_code == 201:
                print("Kafka Connector created successfully.")
            else:
                print(
                    f"Failed to create Kafka Connector. Status code: {response.status_code}"
                )
                print(response.text)

    def name_connectors(self, kafka_connect_url: str, name: str = None):
        headers = {"Content-Type": "application/json"}
        output = []
        url = "{kafka_connect_url}/connectors".format(
            kafka_connect_url=kafka_connect_url
        )
        # Send a POST request to create the Kafka Connector
        if name:
            url = url + "/{name}".format(name=name)

        response = requests.get(url, headers=headers)

        # Check the response
        if response.status_code == 200:
            if name:
                output = [response.json()]
            else:
                data = sorted(response.json())
                output = [item for item in data]
        else:
            print(
                f"Failed to create Kafka Connector. Status code: {response.status_code}"
            )
            print(response.text)

        return output
    


    def delete_connector_by_prefix(self, kafka_connect_url: str, prefix: str = None):
        headers = {"Content-Type": "application/json"}
        output = []
        url = "{kafka_connect_url}/connectors".format(
            kafka_connect_url=kafka_connect_url
        )

        match_connectors = self.name_connectors(kafka_connect_url)

        # Send a POST request to create the Kafka Connector
        urls = [url + "/{conn}".format(conn=conn) for conn in match_connectors if conn.startswith(prefix)]
        
        for u in urls:
            response = requests.delete(u, headers=headers)
            
            if response.status_code == 204:
                print(u, " exclui com sucesso...")

            else:
                print(
                    f"Failed to create Kafka Connector. Status code: {response.status_code}"
                )
                print(response.text)

if __name__ == "__main__":
    # Configurando o parser
    parser = argparse.ArgumentParser(description="Criação de topicos")

    parser.add_argument(
        "ct",
        choices=["create_sink_connectors", "list_topics", "name_connectors", "delete_connectors"],
        help="Criar topicos",
    )
    parser.add_argument("-b", "--broker", type=str, help="Endereço do broker")
    parser.add_argument(
        "-f", "--file", type=str, help="Nome do arquivo de configuracao"
    )
    parser.add_argument("-p", "--prefix", type=str, help="Prefixo do topico")
    parser.add_argument("--connect_url", type=str, help="Link Kafka Connect")
    parser.add_argument("-nc", "--name_connector", type=str, help="Link Kafka Connect")


    args = parser.parse_args()

    if "list_topics" in args.ct:
        settings = Settings(broker=args.broker)
        print(settings.list_topics_by_prefix(args.prefix))

    if "name_connectors" in args.ct:
        if args.connect_url:
            settings = Settings()
            if args.name_connector:
                pprint(settings.name_connectors(args.connect_url, args.name_connector) )
            else:
                print("\n".join(settings.name_connectors(args.connect_url)))

    if "delete_connectors" in args.ct:
        if args.connect_url and args.prefix:
            settings = Settings()
            settings.delete_connector_by_prefix(args.connect_url, args.prefix)


    if "create_sink_connectors" in args.ct:
        if args.broker and args.file:
            if Path(args.file).exists():
                if args.prefix is not None:
                    settings = Settings(
                        path=args.file, broker=args.broker, prefix=args.prefix
                    )
                    settings.create_sink_connectors()
                else:
                    settings = Settings(path=args.file, broker=args.broker)
                    settings.create_sink_connectors()
