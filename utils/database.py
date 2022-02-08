from cgi import print_directory
from functools import cache
from tkinter.messagebox import NO
import pymysql
from settings import DATABASE_CONFIG


class DBHandler:
    def __init__(self):
        self.config = DATABASE_CONFIG
    

    def connect(self):
        self.db = pymysql.connect(  
            host=self.config['HOST'], 
            port=self.config['PORT'], 
            user=self.config['USER'], 
            password=self.config['PASSWORD'], 
            database=self.config['DB'], 
            charset='utf8' 
        )


    def session(self, query):
        self.connect()

        try:
            with self.db.cursor() as cursor:
                if cursor is None:
                    return "empty db"
                elif cursor.rowcount == 0:
                    return "empty db"
                else:
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
        except:
            return "empty db"
        finally:
            self.db.close()


    def Open(self):
        try:
            if self.db.cursor().rowcount == 0:
                print("cursor none")
            else:
                self.cursor = self.db.cursor()
        except pymysql.err.IntegrityError as ITE:
            print(ITE.args)
        except pymysql.err.OperationalError as OE:
            print(OE.args)
        except pymysql.err.InternalError as IE:
            print(IE.args)


    def Close(self):
        try:
            if self.cursor.rowcount == 0:
                print("cursor none")
            else:
                self.cursor.close()
                self.db.close()
        except pymysql.err.OperationalError as OE:
            print(OE.args)
        except pymysql.err.InternalError as IE:
            print(IE.args)

    
    def Execute(self, query) -> tuple[str]:
        try:
            if self.cursor.rowcount != 0:
                self.cursor.execute(query)
                return self.cursor.fetchall()
        except pymysql.err.IntegrityError as ITE:
            print(ITE.args)
            return ITE.args
        except pymysql.err.ProgrammingError as PE:
            print(PE.args)
            return PE.args
        finally:
            self.Close()
            
