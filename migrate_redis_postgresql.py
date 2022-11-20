import psycopg2
from redis import Redis


# Connect to dbs
rdb = Redis(host="localhost", port=6379)
conn = psycopg2.connect("dbname=alibrary")
cur = conn.cursor()

keys = rdb.keys(':Ali:*')

cur.execute("CREATE EXTENSION pg_jieba;")
# share_id is of length 11, file_id is of length 40, separete by a ':'
cur.execute("CREATE TABLE record (id char(52) PRIMARY KEY, name TEXT, size INTEGER, tsv TSVECTOR GENERATED ALWAYS AS (to_tsvector('jiebacfg', name)) STORED);")
for key in keys:
    print(key)
    cur.execute("INSERT INTO record (id, name, size) VALUES (%s, %s, %s);",
                (key.decode()[5:], rdb.hget(key, 'n').decode('utf-8'), int(rdb.hget(key, 's').decode())))

cur.execute("CREATE INDEX record_idx ON record USING GIN (tsv);")
# Retrieve query results
conn.commit()
cur.close()
conn.close()
