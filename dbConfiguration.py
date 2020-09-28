#this module is used for database connection and querying

import psycopg2
import random

class DbConfig:
    def __init__(self, db_ip, db_name, db_port, db_username, db_password):
        self.db_ip = db_ip
        self.db_name = db_name
        self.db_port = db_port
        self.db_username = db_username
        self.db_password = db_password
        self.comboUsed = []


    def ConnectDb(self):  # self,db_ip,db_name, db_port, db_username, db_password):
        try:
            self.conn = psycopg2.connect(
                "dbname='" + self.db_name + "' user='" + self.db_username + "' host='" + self.db_ip + "' password='" + self.db_password + "' port=" + str(
                    self.db_port) + ")")
            return True
        except Exception as e:
            return False

    def returnedFormattedQuery(self, query, vare = None):
        cursor = self.conn.cursor()
        result = cursor.mogrify(query, vare)
        cursor.close()
        return result

    def DbResultsQuery(self, query, vare=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, vare)
            print(cursor.mogrify(query, vare))
            res = cursor.fetchall()
            cursor.close()
            return res
        except Exception as e:
            print(e)
            self.refreshDbConenction()

    def DbModifyQuery(self,query, vare=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, vare)
            cursor.close()
            self.conn.commit()
        except:
            self.refreshDbConenction()
    def commitConnection(self):
        self.conn.commit()

    def releaseDbConnection(self):
        self.conn.close()

    def DbResultsQueryForFunction(self, query, vare=None):
        cursor = self.conn.cursor()
        cursor.execute(query, vare)
        res = cursor.fetchall()
        cursor.close()
        self.conn.commit()
        return res


    def refreshDbConenction(self):
        try:
            self.releaseDbConnection()
        except:
            pass
        self.ConnectDb()
