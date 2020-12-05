from sqlalchemy import Column, Integer, ForeignKey, Text, Float , Boolean , Date , Index, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.indexable import index_property

Base = declarative_base()

class User_group(Base):
    __tablename__ = "user_group"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('group.id'), nullable=False)

    def __init__(self , user_id , group_id):
        self.user_id = user_id
        self.group_id = group_id

class Post_group(Base):
    __tablename__ = "post_group"
    id = Column(Integer , primary_key=True)
    post_id = Column(Integer ,  ForeignKey('post.id') , nullable= False)
    group_id = Column(Integer , ForeignKey('group.id'), nullable=False)

    def __init__(self , post_id , group_id):
        self.post_id = post_id
        self.group_id = group_id

class Group(Base):
    __tablename__ = "group"
    id = Column(Integer , primary_key=True)
    name = Column(Text , nullable=False)
    description = Column(Text , nullable=False)
    post = relationship("Post" , secondary = "post_group")
    user = relationship("User" , secondary = "user_group")

    def __init__(self, name, description):
        self.name = name
        self.description = description

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer , primary_key=True)
    text = Column(Text , nullable=False)
    views = Column(Integer , nullable=False)
    user_id = Column(Integer , ForeignKey("user.id"), nullable=True)
    group = relationship("Group" , secondary = "post_group")
    user = relationship("User")

    def __init__(self , text, views, user_id):
        self.text = text
        self.views = views
        self.user_id = user_id

class User(Base):
    __tablename__ = "user"
    id = Column(Integer , primary_key=True)
    email = Column('email', String(30) , nullable=False)
    password = Column('password' ,String(30) , nullable=False)
    group = relationship("Group" , secondary = "user_group")

    def __init__(self , email, password):
        self.email = email
        self.password = password