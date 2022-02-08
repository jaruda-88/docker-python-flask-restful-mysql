from cgi import print_directory
from functools import cache
from tkinter.messagebox import NO
import pymysql
from settings import DATABASE_CONFIG


class DBHandler:
    def __init__(self):
        try:
            config = DATABASE_CONFIG
            self.db = pymysql.connect(  
                                        host=config['HOST'], 
                                        port=config['PORT'], 
                                        user=config['USER'], 
                                        password=config['PASSWORD'], 
                                        database=config['DB'], 
                                        charset='utf8'
                                    )
        except pymysql.err.MySQLError as ME:
            print(ME.args)
        except pymysql.err.DatabaseError as DE:
            print(DE.args)
        except pymysql.err.OperationalError as OE:
            print(OE.args)


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
            
