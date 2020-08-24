from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
# baseを使って、テーブルクラスを使う
Base = declarative_base()


class User(Base):
    """
    Userテーブルクラス
    """
    # テーブル名
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:')
meta = Base.metadata
meta.create_all(engine)

# セッション
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# insert
suzuki = User(name="Suzuki", age=19)
session.add(suzuki)
suzuki = User(name="name1", age=21)
session.add(suzuki)
suzuki = User(name="name2", age=19)
session.add(suzuki)
suzuki = User(name="name3", age=19)
session.add(suzuki)
session.commit()

# select
print("==============================")
users_obj = session.query(User).all()
print(users_obj)
print("==============================")
suzuki = session.query(User).get(1)
print(suzuki)
print("==============================")
suzuki = session.query(User).get(1)
suzuki.age = 20
session.add(suzuki)
session.commit()
print("==============================")
session.delete(suzuki)
print("==============================")
users_obj = session.query(User).all()
print(users_obj)
print("==============================")
# select * from users where name="Suzuki"
users = session.query(User).filter_by(name="name1").all()
print(users)
print("==============================")
# select * from users where age=21 limit 1;
users = session.query(User).filter_by(age=21).limit(1).all()
print(users)
print("==============================")
# select * from users where age=21 order by name;
users = session.query(User).filter_by(age=21).order_by(User.name).all()
print(users)
print("==============================")
user = session.query(User).filter_by(age=21).order_by(User.name).first()
print("==============================")
user_cnt = session.query(User).filter_by(age=21).count()
print("==============================")
# whereはfilterを。
users = session.query(User).filter(User.age == 19).all()
print("==============================")
from sqlalchemy import and_
users = session.query(User).filter(and_(User.name == 'name2', User.age == 19)).all()
print("==============================")
from sqlalchemy import or_
users = session.query(User).filter(or_(User.name == 'Suzuki', User.age == 21)).all()
print("==============================")
users = session.query(User).filter(User.age.in_([19, 21])).all()
for user in users:
    print(user.id)
    print(user.name)
print("==============================")
print("==============================")

