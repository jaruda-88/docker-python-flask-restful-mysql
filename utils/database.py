pass
# import pymysql
# from utils.settings import DATABASE_CONFIG


# class DBHandler:
#     def __init__(self):
#         """ mysql database controler """
#         self.config = DATABASE_CONFIG

    
#     def connector(self):
#         """ db connector """
#         try:
#             db = pymysql.connect(  
#                     host=self.config['host'], 
#                     port=self.config['port'], 
#                     user=self.config['user'], 
#                     password=self.config['pw'], 
#                     database=self.config['db_name'], 
#                     charset='utf8' 
#                 )
#             return True, db 
#         except pymysql.err.DatabaseError as DE:
#             return False, DE.args
#         except pymysql.err.OperationalError as OE:
#             return False, OE.args


#     def query(self, query, value = ''):
#         """ db connect query """
#         is_connected, db = self.connector()

#         if is_connected:
#             try:
#                 with db.cursor(pymysql.cursors.DictCursor) as cursor:
#                     if value == '':
#                         cursor.execute(query)
#                     else:
#                         cursor.execute(query, value)
#                     result = cursor.fetchall()

#                     cursor.close()
#                 db.close()

#                 return True, result
#             except pymysql.err.MySQLError as ME:
#                 return False, ME.args
#         else:
#             return is_connected, db


#     def executer(self, query, value = ''):
#         """ db connect execute """
#         is_connected, db = self.connector()

#         if is_connected:
#             result = -1
#             try:
#                 with db.cursor(pymysql.cursors.DictCursor) as cursor:                    
#                     if value == '':
#                         result = cursor.execute(query)
#                     else:
#                         result = cursor.execute(query, value)
#                     db.commit()

#                     cursor.close()
#                 db.close()

#                 return True, result

#             except pymysql.err.MySQLError as ME:
#                 return False, ME.args
#         else:
#             return is_connected, db    


#     def querys(self, query_list : list, value_list=None):
#         """ db connect query roop"""
#         is_connected, db = self.connector()

#         if is_connected:
#             try:
#                 result = []
#                 with db.cursor(pymysql.cursors.DictCursor) as cursor:
#                     query_count = len(query_list)
#                     for i in range(query_count):
#                         query = query_list[i]
#                         is_count = True if 'COUNT(id) AS count' in query else False
#                         if type(value_list) is list:
#                             cursor.execute(query) if value_list[i] == '' else cursor.execute(query, value_list[i])
#                         elif value_list is None: 
#                             cursor.execute(query)
#                         else:
#                             cursor.execute(query, value_list)
                        
#                         if is_count:
#                             result.append(cursor.fetchall()[0]['count'])
#                         else:
#                             result.append(cursor.fetchall())
#                     cursor.close()
#                 db.close()

#                 return True, result
#             except pymysql.err.MySQLError as ME:
#                 return False, ME.args
#         else:
#             return is_connected, db
