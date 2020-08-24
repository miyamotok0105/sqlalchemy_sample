from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
# DB接続
engine = create_engine('sqlite:///:memory:')
 
Base = declarative_base()
 
 
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
 
    posts = relationship("Post", backref="users")    # Postとのリレーション
 
 
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    body = Column(Integer)
 
    user = relationship("User")    # Userとのリレーション
 
# テーブルクラスのテーブルを生成
Base.metadata.create_all(engine)
 
# セッション生成
Session = sessionmaker(bind=engine)
session = Session()
 
# サンプルデータ挿入
session.add(User(id=1, name="Suzuki", age=19))
session.add(User(id=2, name="Tanaka", age=21))
session.add(User(id=3, name="Sato", age=21))
 
session.add(Post(users_id=1, title="朝の体操", body="ラジオ体操で元気いっぱい"))
session.add(Post(users_id=1, title="今日の夕食", body="カレーラスがとても美味しかった。"))
session.add(Post(users_id=2, title="仕事", body="今日はDjangoでAPI作成。"))
session.add(Post(users_id=2, title="Python楽しい", body="Python楽しいですよね！！"))
session.commit()
 
# inner joinのサンプル
users = session.query(User).join(Post, User.id == Post.users_id).all()
 
for user in users:
    print("%sさんの投稿" % (user.name))
    for post in user.posts:
        print("|- タイトル：%s" % (post.title,))
    print('')