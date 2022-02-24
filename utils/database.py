import pymysql
from settings import DATABASE_CONFIG


class DBHandler:
    def __init__(self):
        """ mysql database controler """
        print('mysql database controler')


    def connector(self):
        """ db connector """
        try:
            db = pymysql.connect(  
                    host=DATABASE_CONFIG['HOST'], 
                    port=DATABASE_CONFIG['PORT'], 
                    user=DATABASE_CONFIG['USER'], 
                    password=DATABASE_CONFIG['PASSWORD'], 
                    database=DATABASE_CONFIG['DB'], 
                    charset='utf8' 
                )
            return True, db 
        except pymysql.err.DatabaseError as DE:
            return False, DE.args
        except pymysql.err.OperationalError as OE:
            return False, OE.args


    def query(self, query):
        """ db connect query """
        is_connected, db = self.connector()

        if is_connected:
            try:
                with db.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()

                    cursor.close()
                db.close()

                return True, result
            except pymysql.err.MySQLError as ME:
                return False, ME.args
        else:
            return is_connected, db


    def executer(self, query):
        """ db connect execute """
        is_connected, db = self.connector()

        if is_connected:
            try:
                with db.cursor() as cursor:
                    cursor.execute(query)
                    cursor.commit()

                    cursor.close()
                db.close()

                return True, ('success')

            except pymysql.err.MySQLError as ME:
                return False, ME.args
        else:
            return is_connected, db    
