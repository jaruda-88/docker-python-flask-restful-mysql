import re
import pymysql
from utils.settings import DATABASE_CONFIG


class DBHandler:
    def __init__(self):
        """ mysql database controler """
        self.config = DATABASE_CONFIG

    
    def connector(self):
        """ db connector """
        try:
            db = pymysql.connect(  
                    host=self.config['HOST'], 
                    port=self.config['PORT'], 
                    user=self.config['USER'], 
                    password=self.config['PASSWORD'], 
                    database=self.config['DB'], 
                    charset='utf8' 
                )
            return True, db 
        except pymysql.err.DatabaseError as DE:
            return False, DE.args
        except pymysql.err.OperationalError as OE:
            return False, OE.args


    def query(self, query, value = ''):
        """ db connect query """
        is_connected, db = self.connector()

        if is_connected:
            try:
                with db.cursor(pymysql.cursors.DictCursor) as cursor:
                    if value == '':
                        cursor.execute(query)
                    else:
                        cursor.execute(query, value)
                    result = cursor.fetchall()

                    cursor.close()
                db.close()

                return True, result
            except pymysql.err.MySQLError as ME:
                return False, ME.args
        else:
            return is_connected, db


    def executer(self, query, value = ''):
        """ db connect execute """
        is_connected, db = self.connector()

        if is_connected:
            result = -1
            try:
                with db.cursor(pymysql.cursors.DictCursor) as cursor:                    
                    if value == '':
                        result = cursor.execute(query)
                    else:
                        result = cursor.execute(query, value)
                    db.commit()

                    cursor.close()
                db.close()

                return True, result

            except pymysql.err.MySQLError as ME:
                return False, ME.args
        else:
            return is_connected, db    


    def query_paging(self, query_list : str, query_count : str, value : tuple):
        """ db connect query and count inclue"""
        is_connected, db = self.connector()

        if is_connected:
            try:
                with db.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute(query_list, value)
                    list = cursor.fetchall()

                    cursor.execute(query_count, value[0])
                    count = cursor.fetchall()

                    result = {'count': int(count[0]['COUNT(*)']), 'list' : list}

                    cursor.close()
                db.close()

                return True, result
            except pymysql.err.MySQLError as ME:
                return False, ME.args
        else:
            return is_connected, db
