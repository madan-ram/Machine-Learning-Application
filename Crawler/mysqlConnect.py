import MySQLdb as my

class mysqlConnection:
	db=""
	def getConnection(self,dbName):
		self.db = my.connect("localhost","root","1992221",dbName);
		return self.db
		
	def closeConnection(self):
		return self.db.close()
