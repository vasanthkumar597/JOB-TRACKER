from sqlalchemy import Column,Integer,String,ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String,unique=True)
    password=Column(String)
    role=Column(String,default="user")
    
    
    jobs =relationship("Job",back_populates="user")


class Job(Base):
    __tablename__="jobs"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    company=Column(String)
    status=Column(String,default="applied")
    salary=Column(String,nullable=True)

    user_id=Column(Integer,ForeignKey("users.id"))

    user=relationship("User",back_populates="jobs")


