from sqlalchemy import create_engine

# mysql
# from sqlalchemy import create_engine
# engine = create_engine('mysql://scott:tiger@localhost/foo')

# postgreSQL
# pip install psycopg2
# from sqlalchemy import create_engine
# engine = create_engine('postgresql://ユーザー名:パスワード@ホスト:ポート/DB名')

# sqlite
# from sqlalchemy import create_engine
# engine = create_engine('sqlite:///sqliteファイル')

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:')


with engine.connect() as con:
    con.execute("DROP TABLE IF EXISTS USERS")
    con.execute("CREATE TABLE USERS(id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    # データ
    rows = ({"id": 1, "name": "Sato", "age": 31},
            {"id": 2, "name": "Suzuki", "age": 18},
            {"id": 3, "name": "Yamada", "age": 40},
            {"id": 4, "name": "Kuro", "age": 30},
            )
    for row in rows:
        # **のコロン記号をSQLの変数として指定する。
        con.execute("INSERT INTO USERS (id, name, age) VALUES(:id, :name, :age)", **row)
    rows = con.execute("SELECT * FROM USERS")
    for row in rows:
        print(row)
    con.execute("UPDATE USERS SET age=42 WHERE id = :id", **{"id": 3})
    con.execute("DELETE FROM USERS WHERE id = :id", **{"id": 4})
    print("***** 更新後 *****")
    rows = con.execute("SELECT * FROM USERS")
    for row in rows:
        print(row)
