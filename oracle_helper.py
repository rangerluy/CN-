# _*_ coding:utf-8 _*_
import cx_Oracle
import os
import readconfig
os.environ['NLS_LANG']= 'SIMPLIFIED CHINESE_CHINA.UTF8'

#connection_str = 'drgs/drgs@10.68.4.53:1521/hdw'
test = readconfig.ReadConfig()
connection_str = test.get_db("ORACLE_DB", "conn_str")

def get_table_in():
    r = readconfig.ReadConfig()
    t = r.get_db("TABLES", "t_in")
    return t

def get_table_out():
    r = readconfig.ReadConfig()
    t = r.get_db("TABLES", "t_out")
    return t


class OracleHelper:
    """ cx_Oracle 帮助类 """
    def __enter__(self):
        self.__db = cx_Oracle.connect(connection_str)
        self.__cursor = self.__db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cursor.close()
        self.__db.close()

    def execute_query(self, sql, params=None):
        """ 查询逻辑(有参和无参) """
        try:
            if params is None or params is '':
                result = self.__cursor.execute(sql)
            else:
                result = self.__cursor.execute(sql, params)
        except cx_Oracle.DatabaseError as err:
            print(sql, params)
            raise err
        return result

    #added by lfc 20190606
    def query_fetchone(self, sql, params=None):
        """ 查询逻辑(有参和无参)，只返回一个结果 """
        try:
            if params is None or params is '':
                self.__cursor.execute(sql)
            else:
                self.__cursor.execute(sql, params)

            result = self.__cursor.fetchone()[0]
        except cx_Oracle.DatabaseError as err:
            print(sql, params)
            raise err
        return result


    def fetchmany(self, n):
        try:
            result = self.__cursor.fetchmany(n)
        except cx_Oracle.DatabaseError as err:
            print(n)
            raise err
        return result

    def fetchone(self):
        try:
            result = self.__cursor.fetchone()
        except cx_Oracle.DatabaseError as err:
            raise err
        return result


    def execute_sql(self, sql, params=None):
        """ 增、删、改逻辑 """
        self.__db.begin()
        try:
            if params is None or params is '':
                result = self.__cursor.execute(sql)
            else:
                result = self.__cursor.execute(sql, params)
        except cx_Oracle.DatabaseError as err:
            self.__db.rollback()
            print(sql, params)
            raise err

        self.__db.commit()

    def execute_sql_many(self, sql, params):
        """ 批量操作 """
        self.__db.begin()
        try:
            result = self.__cursor.executemany(sql, params)
        except cx_Oracle.DatabaseError as err:
            self.__db.rollback()
            print("error:execute_sql_many")
            # print(params)
            # for i in params:
            #     print(i,"params---")
            raise err

        self.__db.commit()

    def execute_proc(self, sql):
        try:
            result = self.__cursor.callproc(sql)
        except cx_Oracle.DatabaseError as err:
            raise err


if __name__ == '__main__':

    # sqlMsg = ''' select count(1) from d_in_msg  '''
    #
    # with OracleHelper() as oracle_h:
    #     ret = oracle_h.query_fetchone(sqlMsg)
    #     print(ret)

    table_in = get_table_in()

    sqlMsg = ''' select * from %s ''' % (table_in)

    with OracleHelper() as oracle_h:
        oracle_h.execute_query(sqlMsg)


        rows = oracle_h.fetchmany(3)

        while rows:

            for row in rows:
                print(row)

            rows = oracle_h.fetchmany(3)




        # row = oracle_h.fetchone()
        #
        # while row:
        #     print(row)
        #     row = oracle_h.fetchone()

    #
    #
    # db = cx_Oracle.connect(connection_str)
    # cursor = db.cursor()
    # rows = cursor.execute(sqlMsg)
    #
    # row = cursor.fetchone()
    #
    # while row:
    #     print(row)
    #     row = cursor.fetchone()
    #
    # cursor.close()
    # db.close()