from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey, MetaData, create_engine
from sqlalchemy.sql import select, insert, update, delete, join
from sqlalchemy.sql import asc
from sqlalchemy import and_, or_, tuple_

engine = create_engine('sqlite:///:memory:')
meta = MetaData(engine, reflect=True)
meta.bind = engine
users = Table('Users', meta,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('age', Integer)
              )
posts = Table('Posts', meta,
              Column('id', Integer, primary_key=True),
              Column('user_id', ForeignKey("Users.id")),
              Column('title', String),
              Column('body', Text)
              )
meta.create_all()


# sqlぽくラップしてくれる機能がある。
# selって言ってる。

with engine.connect() as con:
    print("==============================")
    print("insert")
    sel_insert = insert(users, values=({"id": 1, "name": 'Suzuki', "age": 20},
                                       {"id": 2, "name": 'Tanaka', "age": 33},
                                       {"id": 3, "name": 'Tanaka2', "age": 40},
                                       {"id": 4, "name": 'Tanaka3', "age": 50},
                                       {"id": 5, "name": 'Tanaka4', "age": 60},))
    result = con.execute(sel_insert)
    print(result.rowcount)

    print("==============================")
    print("update")
    sel_update = update(users, users.c.name == 'Suzuki')
    con.execute(sel_update, id=10)

    print("==============================")
    print("delete")
    sel_delete = delete(users, users.c.id == 2)
    con.execute(sel_delete)

    print("==============================")
    print("select")
    # select id, name from users where id = 1 limit 3;
    sel_select = select([users.c.id, users.c.name]).limit(3)
    result = con.execute(sel_select)
    for row in result:
        print(row)

    print("==============================")
    # where and
    sel_select = select([users]).where(and_(users.c.age > 18, users.c.age < 60))
    result = con.execute(sel_select)
    for row in result:
        print(row)
    print("==============================")
    # where or
    sel_select = select([users]).where(or_(users.c.age > 18, users.c.age < 60))
    result = con.execute(sel_select)
    for row in result:
        print(row)
    print("==============================")
    # order
    sel_select = select([users]).order_by(asc(users.c.name))
    result = con.execute(sel_select)
    for row in result:
        print(row)
    print("==============================")
    # like句
    sel_select = select([users]).where(users.c.name.like('%zuki%'))
    result = con.execute(sel_select)
    for row in result:
        print(row)
    print("==============================")
    # in句
    user_id_conditions = [(1,), (2,), (3,), (8,)]
    sel_select = select([users]).where(tuple_(users.c.id).in_(user_id_conditions))
    result = con.execute(sel_select)
    for row in result:
        print(row)
    print("==============================")
    post_insert = insert(posts, values=({"id": 1, "user_id": 1, "title": "Sample", "body": "記事本文"},))
    con.execute(post_insert)
    # left join
    sel_join = select([users.join(posts)])
    result = con.execute(sel_join)
    for row in result:
        print(row)
    print("==============================")

