from confluent_kafka.admin import AdminClient, ConfigResource
from confluent_kafka import Consumer, KafkaError
import json
import re
from pathlib import Path
import yaml
import requests
import sys

PATH_CONFIG = "./client1_settings.yml"

class Settings:
    def __init__(self, path: str = None) -> None:
        _path = path if path else PATH_CONFIG

        if Path(_path).exists():
            with open(Path(PATH_CONFIG), "r") as file:
                self.data = yaml.load(file, Loader=yaml.FullLoader)

            self.KAFKA_CONNECT_URL = self.data["settings"]["kafka_connect_url"]
            self.CLIENT_PREFIX = self.data["settings"]["client_prefix"]
            self.PATH_TEMPLATE = self.data["settings"]["path_template"]
            self.DATASOURCE = {
                "JDBC_URL": self.data["settings"]["datasource"]["jdbc_url"],
                "USER": self.data["settings"]["datasource"]["user"],
                "PASSWORD": self.data["settings"]["datasource"]["password"],
                "TABLES-MAP": {
                    table["table"]: {"pks": table["pks"]}
                    for table in self.data["settings"]["datasource"]["tables-map"]
                },
            }

        else:
            print("Arquivo não existente no caminho: ", PATH_CONFIG)


settings = Settings()


def read_sink_template(path):
    path_file = Path(path)
    if path_file.exists():
        with open(path_file, "r") as file:
            data = json.load(file)
            return data
    else:
        print("Arquivo não existente no caminho: ", path)


def list_topics_by_prefix(prefix):
    """Lista os topicos do Broker de acordo com o prefixo, e um objeto de mapemaneto de acordo com os topicos encontrados

    Args:
        prefix (str): prefixo para procurar nos topicos

    Returns:
        list[dict{table: <name_of_table>, topic: name_of_topic}]: retorna uma lista de dicionarios com esse mapeamento de tabela e topico
    """

    admin_client = AdminClient({"bootstrap.servers": "localhost:9092"})

    topic_metadata = admin_client.list_topics()

    matching_topics = [
        topic for topic in topic_metadata.topics if topic.startswith(prefix)
    ]

    return matching_topics


def match_map_topic(topic_names):
    pattern = r"\.([^\.]+)$"
    tables = settings.DATASOURCE["TABLES-MAP"].keys()
    tables_map = settings.DATASOURCE["TABLES-MAP"]

    for topic in topic_names:
        match = re.search(pattern, topic)
        if match:
            if match.group(1) in tables:
                tables_map[match.group(1)]["topic"] = topic
        else:
            print("No match topic; " + topic)

    return tables_map


def format_sink_templates(path_template, match_topics):
    templates = []

    for t in match_topics.keys():        
        template = read_sink_template(path_template)
        template["config"]["topics"] = match_topics[t]["topic"]
        template["config"]["connection.url"] = settings.DATASOURCE["JDBC_URL"]
        template["config"]["connection.username"] = settings.DATASOURCE["USER"]
        template["config"]["connection.password"] = settings.DATASOURCE["PASSWORD"]
        template["config"]["table.name.format"] = t
        template["config"]["primary.key.fields"] = ", ".join(match_topics[t]["pks"])
        template["name"] = match_topics[t]["topic"] + "-dbz-sink-conn"
        templates.append(template)

    return templates


def create_topic(templates):
    # Define the headers for the HTTP request
    headers = {"Content-Type": "application/json"}

    for template in templates:
        json_template = json.dumps(template)

        # Send a POST request to create the Kafka Connector
        response = requests.post(
            f"{settings.KAFKA_CONNECT_URL}/connectors",
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


def delete_topics(topics):
    """delete topics"""

    # Call delete_topics to asynchronously delete topics, a future is returned.
    # By default this operation on the broker returns immediately while
    # topics are deleted in the background. But here we give it some time (30s)
    # to propagate in the cluster before returning.
    #
    # Returns a dict of <topic,future>.

    admin_client = AdminClient({"bootstrap.servers": "192.168.0.226:9092"})

    fs = admin_client.delete_topics(topics, operation_timeout=30)

    # Wait for operation to finish.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} deleted".format(topic))
        except Exception as e:
            print("Failed to delete topic {}: {}".format(topic, e))


if __name__ == "__main__":
    topics = list_topics_by_prefix(settings.CLIENT_PREFIX)
    print(topics)

    match_topics = match_map_topic(topics)
    print(match_topics)

    # sink_templates = format_sink_templates(settings.PATH_TEMPLATE, match_topics)

    # create_topic(sink_templates)

    # print(sys.argv)

    # operation = sys.argv[1]    
    # args = sys.argv[2:]

    # osmap = {
    #     "create_topic": create_topic,
    # }


    # if operation not in osmap:
    #     sys.stderr.write("Unknow operation: %s\n" % operation)

        
    # osmap[operation](args)