import mysql.connector
from mysql.connector import errorcode


class DBHandler():
    def __init__(self, user:str, pw:str, host:str, database:str, port=3306, raise_on_warnings=True, use_pure=False):
        ''' init create config '''
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
        ''' config edit '''
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
        ''' mysql connector\n
        error -> raise Exception(error message)
        return db connector obj'''
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
        ''' mysql SELECT\n
        param -> sql = sql\n 
        param -> value = Condition, type(tuple)\n
        param -> all = True(fetchall)/False(fetchone)\n
        param -> dict = True(dictionary result)/False(result)\n
        error -> raise Exception(error message)\n
        return result query'''
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


    def querys(self, datas:list, dict=True):
        ''' mysql curd\n
        param -> datas = [
                {
                    'sql': 'SELECT * FROM tb;',
                    'value': None,
                    'op': {'type': 'query', 'all': True}
                },
                {
                    'sql': 'UPDATE tb SET value1=%s value2=%s',
                    'value': ('test', 'test'),
                    'op': {'type': 'executer', 'last_id': False}
                }
            ]\n
        error -> raise Exception(error message)\n
        return Result query list of input array order
        '''
        try:
            conn = self.connector()            
            with conn.cursor(dictionary=dict) as cursor:
                result = []
                for data in datas:
                    option = data['op']
                    sql = data['sql']
                    value = data['value']
                    type = option['type']
                    if type == 'query':
                        all = option['all']
                        cursor.execute(sql, value) if value else cursor.execute(sql)
                        result.append(cursor.fetchall() if all else cursor.fetchone())
                    elif type == 'executer':
                        last_id = option['last_id']
                        cursor.execute(sql, value) if value else cursor.execute(sql)
                        if last_id:
                            result.append(cursor.lastrowid) 
                        conn.commit()
                        if last_id == False:
                            result.append(cursor.rowcount)
                    else:
                        raise Exception('datas:op:type error')
        except mysql.connector.Error as err:
            raise Exception(err.msg)
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            cursor.close()
            conn.close()
            return result  

    
    def executer(self, sql, value=None, last_id=False, dict=True):
        ''' mysql cud\n
        param -> sql = sql\n 
        param -> value = Condition, type(tuple)\n
        param -> last_id - True(lastrowid)/False(rowcount)\n
        param -> dict - True(dictionary result)/False(result)\n
        error -> raise Exception(error message)\n
        return execute success(0↑)/fail(0)'''
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