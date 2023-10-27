from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Date
import random
from datetime import datetime, timedelta
import string

COLUMNS = {
    "id": "id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY",
    "descricao": "descricao VARCHAR2(100)",
    "data": "data DATE",
}

GRANTS_CDC = [
    "GRANT SELECT ON {username}.{name} TO C##CDC_PRIVS",
    "GRANT FLASHBACK ON {username}.{name} TO C##CDC_PRIVS",
    "ALTER TABLE {username}.{name} ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS",
]

username = "C##USERSOURCE"
password = "C##USERSOURCE"
host = "192.168.0.226"
port = "1521"
service_name = "ORCLCDB"

# Connection URL format for cx_Oracle
connection_url = (
    f"oracle+cx_oracle://{username}:{password}@{host}:{port}/{service_name}"
)
engine = create_engine(connection_url)

# Define the base class for declarative models
Base = declarative_base()


tables = []


def table_exist(v_table_name):
    stmt = "SELECT COUNT(*) FROM user_tables WHERE table_name = '{name}'".format(
        name=v_table_name
    )
    with engine.connect() as conn:
        result = conn.execute(text(stmt)).scalar()

    return result > 0


def generate_radom_date(
    vcount=500, start_date=datetime(2023, 1, 1), end_date=datetime(2023, 12, 31)
):
    dates = []

    # Generate a random datetime within the specified range

    for _ in range(0, vcount):
        random_timedelta = random.randint(0, (end_date - start_date).total_seconds())
        random_datetime = start_date + timedelta(seconds=random_timedelta)
        dates.append(random_datetime)

    return dates


def generate_random_string(vcount=500, min_length=50, max_length=100):
    strings = []
    for _ in range(0, vcount):
        string_length = random.randint(min_length, max_length)
        characters = string.ascii_uppercase
        random_string = "".join(random.choice(characters) for _ in range(string_length))
        strings.append(random_string)
    return strings


def create_sample_tables(vcount: int, if_exists="append"):
    ddl = []
    stmt_template = "CREATE TABLE {name} (\n {columns} \n)"

    if vcount > 0:
        global tables

        tables = ["TB_" + str(t) for t in range(1, vcount + 1)]

        for p in tables:
            ddl.append(
                stmt_template.format(name=p, columns=",\n".join(COLUMNS.values()))
            )

        with engine.connect() as conn:
            for i, stmt in enumerate(ddl):
                if table_exist(tables[i]) and if_exists == "drop":
                    conn.execute(text("DROP TABLE {name}".format(name=tables[i])))
                    print(tables[i] + " excluica com sucesso..." )
                    
                if not table_exist(tables[i]):
                    conn.execute(text(stmt))
                    print(tables[i] + " criada com sucesso...")
                    
                    for grant in GRANTS_CDC:
                        g = grant.format(username=username, name=tables[i])
                        conn.execute(text(g))
                else:
                    print(tables[i] + " ja existe...")


def insert(vcount_tables, vcount=1000, seconds: int = 30):
    global tables
    
    tables = ["TB_" + str(t) for t in range(1, vcount_tables + 1)]
    
    marks = ", ".join(["?" for i in range(0, len(COLUMNS.keys()))][1:])
    columns = ", ".join([i for i in COLUMNS.keys()][1:])
    params = ", ".join([":" + i for i in COLUMNS.keys()][1:])

    stmt = "INSERT INTO " + "{name}" + "(" + columns + ") " + "VALUES (" + params + ")"

    strings = generate_random_string(vcount)
    dates = generate_radom_date(vcount)

    data_insert = list(zip(strings, dates))

    with engine.connect() as conn:
        for t in tables:
            conn.execute(stmt.format(name=t), data_insert)
            print("Insert " + str(vcount) + " rows in " + t)


create_sample_tables(10, if_exists="append")
insert(vcount_tables=10, vcount=500)
