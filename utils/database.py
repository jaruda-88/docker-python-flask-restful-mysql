import pymysql
from settings import DATABASE_CONFIG


class DBHandler:
    def __init__(self):
        self.config = DATABASE_CONFIG


    def connection(self):
        try:
            db = pymysql.connect(  
                    host=self.config['HOST'], 
                    port=self.config['PORT'], 
                    user=self.config['USER'], 
                    password=self.config['PASSWORD'], 
                    database=self.config['DB'], 
                    charset='utf8' 
                )
                
            return db 
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


    def select(self, query):
        db = self.connection()

        if type(db) is tuple:
            return db
        else:
            try:
                with db.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()        
            except pymysql.err.MySQLError as ME:
                result = ME.args
            except pymysql.err.DatabaseError as DE:
                result = DE.args
            except pymysql.err.OperationalError as OE:
                result = OE.args         
            except pymysql.err.IntegrityError as ITE:
                result = ITE.args
            except pymysql.err.InternalError as IE:
                result = IE.args
            except pymysql.err.ProgrammingError as PE:
                result = PE.args   
            finally:
                db.cursor().close()    
                return result


    # def insert(self, query):
    #     try:
    #         with self.connection() as db:
    #             db.cursor().execute(query)
    #             db.cursor().commit()
    #     except pymysql.err.MySQLError as ME:
    #         return ME.args
    #     except pymysql.err.DatabaseError as DE:
    #         return DE.args
    #     except pymysql.err.OperationalError as OE:
    #         return OE.args         
    #     except pymysql.err.IntegrityError as ITE:
    #         return ITE.args
    #     except pymysql.err.InternalError as IE:
    #         return IE.args
    #     except pymysql.err.ProgrammingError as PE:
    #         return PE.args   
    #     finally:
    #         db.cursor().close()    
    #         return ('success')        

    
    # def update(self, query):
    #     try:
    #         with self.connection() as db:
    #             db.cursor().execute(query)
    #             db.cursor().commit()
    #     except pymysql.err.MySQLError as ME:
    #         return ME.args
    #     except pymysql.err.DatabaseError as DE:
    #         return DE.args
    #     except pymysql.err.OperationalError as OE:
    #         return OE.args         
    #     except pymysql.err.IntegrityError as ITE:
    #         return ITE.args
    #     except pymysql.err.InternalError as IE:
    #         return IE.args
    #     except pymysql.err.ProgrammingError as PE:
    #         return PE.args   
    #     finally:
    #         db.cursor().close()    
    #         return ('success')       


    def session(self, query):
        try:
            db = pymysql.connect(  
                host=self.config['HOST'], 
                port=self.config['PORT'], 
                user=self.config['USER'], 
                password=self.config['PASSWORD'], 
                database=self.config['DB'], 
                charset='utf8' 
            )
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
             return db          
