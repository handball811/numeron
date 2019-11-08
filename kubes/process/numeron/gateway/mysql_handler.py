import os
import MySQLdb

def mysql_handler_factory():
	host = os.environ["PROCESS_STORAGE_NETWORK_SERVICE_HOST"]
	user = os.environ["MYSQL_USER"]
	passwd = os.environ["MYSQL_PASSWORD"]
	db   =os.environ["MYSQL_DATABASE"]
	return MysqlHandler(
		host=host,
		user=user,
		passwd=passwd,
		db=db)

class MysqlHandler:
	def __init__(self,host :str, user :str, passwd :str, db :str, charset :str="utf8mb4"):
		self.__initialize(host, user, passwd, db, charset)

	def __initialize(self,host, user, passwd, db, charset):
		self.__connection = MySQLdb.connect(
			host=host,
			user=user,
			passwd=passwd,
			db=db,
			charset=charset)
		self.__cursor = self.__connection.cursor()
	def __save(self):
		self.__connection.commit()
	def __exec(self, sql :str):
		self.__cursor.execute(sql)
		return self.__cursor
	def exec(self, sql :str):
		sql = sql.strip()
		return self.__exec(sql)
