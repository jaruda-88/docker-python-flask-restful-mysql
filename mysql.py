from functools import cache
from tkinter.messagebox import NO
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
            print("db없음")



    def Open(self):
        try:
            self.cursor = self.db.cursor()
        except:
            print("db없음")


    def Close(self):
        try:
            self.cursor.close()
            self.db.close()
        except:
            print("db없음")

    
    def Execute(self, sql):
        try:
            if self.cursor is not None:
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            else:
                return None
        except:
            print("문법 또는 search 에러")
            
