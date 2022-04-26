import mysql.connector
from mysql.connector import errorcode


class DBHandler():
    def __init__(self, user:str, pw:str, host:str, database:str, port=3306, raise_on_warnings=True, use_pure=False):
        self.config = {
            'user': user,
            'password': pw,
            'host': host,
            'database': database,
            'port': port,
            'raise_on_warnings': raise_on_warnings,
            'use_pure': use_pure
        }
        
    
    def change_config(self, user='', pw='', host='', database='', port=3306, raise_on_warnings=True, use_pure=False):
        if user != '':
            self.config['user'] = user

        if pw != '':
            self.config['password'] = pw

        if host != '':
            self.config['host'] = host

        if database != '':
            self.config['database'] = database

        self.config['port'] = port
        self.config['raise_on_warnings'] = raise_on_warnings
        self.config['user_pure'] = use_pure


    def connector(self):
        try: 
            conn = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Exception("Database does not exist")
            else:
                # error_code = err.errno
                # sql_state = err.sqlstate
                raise Exception(err.msg)
        else:
            return conn 


    def query(self, sql, value=None, all=True, dict=True):
        try:
            conn = self.connector()
            with conn.cursor(dictionary=dict) as cursor:
                cursor.execute(sql, value) if value else cursor.execute(sql)
                # fetchone() select의 결과가 다중 행일 경우 unread result found 에러 발생 
                # 단일 행을 출력하는지 다중 행을 출력하는지를 고려하여 사용할것
                result = cursor.fetchall() if all else cursor.fetchone()
        except mysql.connector.Error as err:
            # error_code = err.errno
            # sql_state = err.sqlstate
            raise Exception(err.msg)
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            cursor.close()
            conn.close()
            return result  


    def querys(self, sql_list, value_list, all=True, dict=True):
        try:
            conn = self.connector()
            with conn.cursor(dictionary=dict) as cursor:
                result = []
                for i in range(len(sql_list)):
                    if value_list[i] == '':
                        cursor.execute(sql_list[i])
                    else:
                        cursor.execute(sql_list[i], value_list[i])

                    if all:
                        result.append(cursor.fetchall())
                    else:
                        result.append(cursor.fetchone())
        except mysql.connector.Error as err:
            # error_code = err.errno
            # sql_state = err.sqlstate
            raise Exception(err.msg)
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            cursor.close()
            conn.close()
            return result  

    
    def executer(self, sql, value=None, last_id=False, dict=True):
        try:
            conn = self.connector()
            with conn.cursor(dictionary=dict) as cursor:
                cursor.execute(sql, value) if value else cursor.execute(sql)
                if last_id:
                    result = cursor.lastrowid
                conn.commit()
                if last_id == False:
                    result = cursor.rowcount
        except mysql.connector.Error as err:
            # error_code = err.errno
            # sql_state = err.sqlstate
            raise Exception(err.msg)
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            cursor.close()
            conn.close()
            return result