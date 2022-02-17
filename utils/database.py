import pymysql
from settings import DATABASE_CONFIG

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


    def executer(self, query):
        """ db connect and query execute """
        is_connected, conn = self.connector()

        if is_connected:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query)

                    if 'select' or 'SELECT' in query:
                        result = cursor.fetchall()    
                    else:
                        result = ()
                        cursor.commit()

                    cursor.close()
                conn.close()

                return True, result

            except pymysql.err.MySQLError as ME:
                return False, ME.args
        else:
            return is_connected, conn    
