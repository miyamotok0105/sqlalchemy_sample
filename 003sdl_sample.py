from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:')

# meta dataでテーブル定義できる
meta = MetaData()
users = Table('Users', meta,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('age', Integer)
              )

print(meta.tables['Users'])
for table in meta.tables:
    print(table)


print(users.columns.name)
print(users.c.name)

for col in users.c:
    print(col)

for pk in users.primary_key:
    print(pk)

print(users.c.id.name)
print(users.c.id.type)
print(users.c.id.nullable)
print(users.c.id.primary_key)

# 接続
meta.bind = engine
# メタデータをDB反映
# テーブル作る
meta.create_all()
with engine.connect() as con:
    rows = ({"id": 1, "name": "Sato", "age": 31},
            {"id": 2, "name": "Suzuki", "age": 18},
            {"id": 3, "name": "Yamada", "age": 40},
            {"id": 4, "name": "Kuro", "age": 30},
            )

    for row in rows:
        con.execute("INSERT INTO USERS (id, name, age) VALUES(:id, :name, :age)", row)
    rows = con.execute("SELECT * FROM USERS")
    for row in rows:
        print(row)
