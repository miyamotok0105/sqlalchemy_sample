from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
 
# DB接続
engine = create_engine('sqlite:///:memory:')
 
# Base
Base = declarative_base()
 
 
# テーブルクラスを定義
class User(Base):
    """
    Userテーブルクラス
    """
 
    # テーブル名
    __tablename__ = 'users'
 
    # 個々のカラムを定義
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
 
 
class Post(Base):
    """
    Postテーブルクラス
    """
 
    # テーブル名
    __tablename__ = 'posts'
 
    # 個々のカラムを定義
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    body = Column(Integer)
 
 
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
users_posts = session.query(User, Post).join(Post, User.id == Post.users_id).all()
 
for user_posts in users_posts:
    print("%sさんの投稿 タイトル：%s" % (user_posts.User.name, user_posts.Post.title,))
 
print('*****')
# left outer joinのサンプル
users_posts = session.query(User, Post).outerjoin(Post, User.id == Post.users_id).all()
 
for user_posts in users_posts:
    if user_posts.Post is not None:
        print("%sさんの投稿 タイトル：%s" % (user_posts.User.name, user_posts.Post.title,))
    else:
        pass
        print("%sさんの投稿 なし" % (user_posts.User.name,))
