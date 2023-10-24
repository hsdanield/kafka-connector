### **ZooKeeper**
**Apache ZooKeeper** é um serviço centralizado para manter informações de configuração, nomear, fornecer sincronização distribuída e fornecer serviços de grupo. No Kafka ele não apenas armazena logs de partição de tópicos e lida com solicitações de consumo/produção como outros agentes, mas também mantém metadados de cluster como IDs e racks de agentes, tópicos, partições, informações de líder e ISR e configurações de todo o cluster e por tópico, como bem como credenciais de segurança. Atualmente ele está sendo substituído pelo **Apache KRaft (Kafka Raft)** e se mantém na instalação apenas por questão de compatibilidade com implementações mais antigas.

### **Confluent Platform Server**
O **Confluent Server** é um componente do **Confluent Platform** que inclui Kafka e recursos comerciais adicionais. A seguir estão alguns dos principais recursos incluídos no Confluent Server:
- Controle de acesso baseado em função (RBAC).
- Armazenamento em camadas Clusters de autobalance.
- Confluent para Kubernetes.

### **Schema Registry**
O **Schema Registry** é um serviço de registro de **esquema RESTful** para gerenciar, armazenar e recuperar seus esquemas **Avro®**, **JSON Schema** e **Protobuf**.
Para saber mais sobre o **Schema Registry**, **[CLIQUE AQUI](https://docs.confluent.io/platform/current/schema-registry/index.html#sr-overview)** !

### **Datagen Source Connector**
O conector Kafka Connect Datagen Source gera mock data para desenvolvimento e teste.

### **Enterprise Control Center**
Centro de controle da plataforma.

## **Ksql DB Server**
Contêm interceptores de monitoramento Confluent. Os interceptores de monitoramento permitem que conectores e consultas SQL coletem as métricas que podem ser visualizadas no Confluent Control Center.

**ksqlDB** é um banco de dados criado especificamente para ajudar os desenvolvedores a criar aplicativos de processamento de fluxo em cima do Apache Kafka.

### **KsqlDB cli**
É o command line interface do Ksql.

### **KsqlDB Examples**
Mock data para o KsqlDB.

### **REST Proxy**
O **Confluent REST Proxy** fornece uma interface RESTful para um cluster Apache Kafka®, facilitando a produção e o consumo de mensagens, a visualização do estado do cluster e a execução de ações administrativas sem usar o protocolo ou clientes Kafka nativos.
Se quiser saber mais sobre o REST Proxy, **[CLIQUE AQUI](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjG_KPp7db6AhUyg5UCHbFMDtQQFnoECBcQAQ&url=https%3A%2F%2Fdocs.confluent.io%2Fplatform%2Fcurrent%2Fkafka-rest%2Fquickstart.html&usg=AOvVaw0bm1TeGaGqT-AiUVji5rZN)** !
Agora que temos uma idéia de todos os compoinentes que fazem parte do Confluent Platform, vamos para instalação !

## **Kafka Connect**
O Kafka Connect é um componente do Apache Kafka usado para realizar a integração de streaming entre o Kafka e outros sistemas, como bancos de dados, serviços em nuvem, índices de pesquisa, sistemas de arquivos e armazenamentos de valores-chave.
O Kafka Connect facilita o fluxo de dados de várias fontes para o Kafka e o fluxo de dados do Kafka para vários destinos.
É nele onde iremos instalar os nossos conectores, que são:
##### **Oracle CDC**
> O Confluent Oracle CDC Source Connector é um conector Premium Confluent e requer uma assinatura adicional, especificamente para este conector. O Oracle CDC Source Connector captura as alterações em um banco de dados Oracle e grava as alterações como registros de eventos de alteração nos tópicos do Kafka.
> 
> O conector usa o Oracle LogMiner para ler o log de redo do banco de dados e requer log complementar com colunas “ALL”. O conector suporta Oracle 11g, 12c, 18c e 19c.
> 
> Ele oferece suporte a bancos de dados de contêiner e bancos de dados que não são de contêiner e oferece suporte a bancos de dados executados no local ou na nuvem. O conector pode ser configurado para capturar um subconjunto das tabelas em um único banco de dados Oracle.
> As tabelas capturadas são todas as tabelas acessíveis pelo usuário que correspondem a um padrão “incluir” e não correspondem a um padrão “excluir” separado. Opcionalmente, o conector pode começar tirando um instantâneo de cada uma das tabelas, para capturar todas as linhas em seu estado atual antes que as alterações sejam registradas.
> O conector continua capturando as alterações individuais em nível de linha confirmadas pelos usuários do banco de dados. Ele grava esses eventos de alteração em tópicos do Kafka usando mapeamento flexível de tabela para tópico.
> Por padrão, todos os eventos de alteração de cada tabela são gravados em um tópico Kafka separado.
> **Fonte:** Confluent Kafka Connect.
##### **JDBC Connector**
Abaixo a explicação traduzida do site da Confluent:
> Os conectores JDBC de origem e coletor permitem a troca de dados entre bancos de dados relacionais e Kafka. O conector de origem JDBC permite importar dados de qualquer banco de dados relacional com um driver JDBC para tópicos do Kafka.
> 
> Ao usar o JDBC, esse conector pode oferecer suporte a uma ampla variedade de bancos de dados sem exigir código personalizado para cada um. Os dados são carregados executando periodicamente uma consulta SQL e criando um registro de saída para cada linha no conjunto de resultados.  
> Por padrão, todas as tabelas em um banco de dados são copiadas, cada uma para seu próprio tópico de saída. O banco de dados é monitorado para tabelas novas ou excluídas e se adapta automaticamente.
> 
> Ao copiar dados de uma tabela, o conector pode carregar apenas linhas novas ou modificadas especificando quais colunas devem ser usadas para detectar dados novos ou modificados. O conector de coletor JDBC permite exportar dados de tópicos Kafka para qualquer banco de dados relacional com um driver JDBC.
> 
> Ao usar o JDBC, esse conector pode suportar uma ampla variedade de bancos de dados sem exigir um conector dedicado para cada um. O conector pesquisa os dados do Kafka para gravar no banco de dados com base na assinatura dos tópicos.  
> É possível obter gravações idempotentes com upserts. A criação automática de tabelas e a evolução automática limitada também são suportadas.  
> 
> **Fonte:** Confluent Kafka Connect

#### Instalando os conectores

**Vamos listar os containers que estão executando:**
```bash
docker compose ps
```

**Copiando os conectores para dentro do container**
```bash
docker cp ./libs/confluentinc-kafka-connect-oracle-cdc-2.7.3.zip connect:/home/appuser

docker cp ./libs/confluentinc-kafka-connect-jdbc-10.7.3.zip connect:/home/appuser
```

**Verificando arquivos dentro do container**
```bash
docker exec -it -u 0 connect /bin/bash
```


Agora vamos para a **instalação** propriamente dita. Comecemos com o **Oracle CDC** utilizando o **[confluent hub](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjWkt7Ngtn6AhVFjZUCHU8QAKoQFnoECA4QAQ&url=https%3A%2F%2Fwww.confluent.io%2Fhub%2F&usg=AOvVaw2WYtBfOfgGmF3P8xPeefkp)**.
```bash
confluent-hub install confluentinc-kafka-connect-oracle-cdc-2.7.3.zip
```
Sequencia de opções: [1, y, y, y]

```bash
confluent-hub install confluentinc-kafka-connect-jdbc-10.7.3.zip
```
Sequencia de opções: [1, y, y, y]

**Saindo do container**
```bash
exit
```

**Precisamos parar todos os containers e iniciá-los novamente**
```bash
docker compose stop
```

```bash
docker compose up -d
```

Acessando o Confluent Platform e verificando se os conectores foram instalados.
- Acessar Connect: Pode ser que demore um pouco para aparecer
http://localhost:9021/

# Criando banco de dados oracle

```bash
git clone https://github.com/oracle/docker-images
```

```shell
cd oracle-docker-images
```

```bash
cd OracleDatabase/SingleInstance/dockerfiles/19.3.0
```

**Linux**
```linux
grep -v ^# db_inst.rsp | grep -v ^$
```

```
grep -v ^# dbca.rsp.tmpl | grep -v ^$
```

**Windows**
```
findstr -v ^# db_inst.rsp | findstr -v ^$
```

```
findstr -v ^# dbca.rsp.tmpl | findstr -v ^$
```

```
./buildContainerImage.sh -v 19.3.0 -e
```

```
cd oracle-docker-images/OracleDatabase/SingleInstance/dockerfiles
```

**Necessário arquivo LINUX.X64_193000_db_home.zip dentro do diretório a seguir:**
```
/oracle-docker-images/OracleDatabase/SingleInstance/dockerfiles/19.3.0/LINUX.X64_193000_db_home.zip
```

**Gerar Container**
```bash
docker run --name oracle19c_1 -p 1521:1521 -p 5500:5500 -e ORACLE_PDB=orcl -e ORACLE_PWD=orcl -e ORACLE_MEM=1000 -v /opt/oracle/oradata -d oracle/database:19.3.0-ee
```
