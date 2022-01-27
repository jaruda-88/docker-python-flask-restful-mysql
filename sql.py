from functools import cache
import pymysql

config = {
    'HOST' : '13.124.47.173',
    'USER' : 'root',
    'PASSWORD' : 'admin',
    'DB' : 'project1',
    'PORT' : 3306,
}

class DBHandler:
    def __init__(self):
        try:
            self.db = pymysql.connect(  
                                        host=config['HOST'], 
                                        port=config['PORT'], 
                                        user=config['USER'], 
                                        password=config['PASSWORD'], 
                                        database=config['DB'], 
                                        charset='utf8'
                                    )
        except:
            print("ddd")



    def Open(self):
        self.cursor = self.db.cursor()


    def Close(self):
        self.cursor.close()
        self.db.close()

    
    def Execute(self, sql):
        try:
            self.cursor.execute(sql)
        finally:
            return self.cursor.fetchall()
