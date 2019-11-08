from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)
from sqlalchemy.ext.declarative import declarative_base
import os

def mysql_handler_factory():
	host = os.environ["MYSQL_HOST"]
	user = os.environ["MYSQL_USER"]
	passwd = os.environ["MYSQL_PASSWORD"]
	db   =os.environ["MYSQL_DATABASE"]
	return MysqlHandler(
		host=host,
		user=user,
		passwd=passwd,
		db=db)

class MysqlHandler:
	def __init__(self, host :str, user :str, passwd :str, db :str, charset :str="utf8mb4"):
		self.__initialize(host, user, passwd, db, charset)

	def __initialize(self,host, user, passwd, db, charset):
		self.__url = "mysql+mysqldb://{}:{}@{}/{}?charset={}".format(user, passwd, host, db, charset)
		self.__engine = create_engine(self.__url, echo=True)
		self.__session = scoped_session(
			sessionmaker(
				autocommit=False,
				autoflush=False,
				bind=self.__engine))
	def get_session(self):
		return self.__session
	def get_engine(self):
		return self.__engine
	def add(self, model_object):
		self.__session.add(model_object)
	def commit(self):
		self.__session.commit()