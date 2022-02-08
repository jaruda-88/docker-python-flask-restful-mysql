from cgi import print_directory
from functools import cache
from tkinter.messagebox import NO
import pymysql
from settings import DATABASE_CONFIG


class DBHandler:
    def __init__(self):
        self.config = DATABASE_CONFIG


    def session(self, query):
        try:
            self.db = pymysql.connect(  
                    host=self.config['HOST'], 
                    port=self.config['PORT'], 
                    user=self.config['USER'], 
                    password=self.config['PASSWORD'], 
                    database=self.config['DB'], 
                    charset='utf8' 
                )
                
            with self.db.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()      
        except pymysql.err.MySQLError as ME:
            return ME.args
        except pymysql.err.DatabaseError as DE:
            return DE.args
        except pymysql.err.OperationalError as OE:
            return OE.args         
        except pymysql.err.IntegrityError as ITE:
            return ITE.args
        except pymysql.err.InternalError as IE:
            return IE.args
        except pymysql.err.ProgrammingError as PE:
            return PE.args
        finally:
             self.db.close()            
