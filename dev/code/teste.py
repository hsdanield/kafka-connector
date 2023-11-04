from sqlalchemy import create_engine
import cx_Oracle

host="localhost"
port=1522
sid='ORCLCDB'
user='SOURCE_C1'
password='SOURCE_C1'
sid = cx_Oracle.makedsn(host, port, sid=sid)

cstr = 'oracle://{user}:{password}@{sid}'.format(
    user=user,
    password=password,
    sid=sid
)

engine =  create_engine(
    cstr,
    convert_unicode=False,
    pool_recycle=10,
    pool_size=50,
    echo=True
)

