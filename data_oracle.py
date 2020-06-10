
from oracle_helper import OracleHelper

# 从oracle 数据库中 取概率
class DataOracle:
    """样本数据类"""

    def __init__(self):
        self.listID = []
        pass


    def query_count(self, table_in, table_out):

        count = 0

        #sqlTrunc = ''' truncate table %s ''' % (table_out)

        sqlMsg = ''' select count(1) from %s t1
            where not exists(select 1 from %s t2 where t2.base_id = t1.base_id)
             and t1.main_diag_code is not null''' % (table_in, table_out)

        with OracleHelper() as oracle_h:
            #oracle_h.execute_sql(sqlTrunc)

            count = oracle_h.query_fetchone(sqlMsg)

        return count

        pass



if __name__ == '__main__':
    from oracle_helper import *

    data_orc = DataOracle()

    table_in = get_table_in()
    table_out = get_table_out()
    count = data_orc.query_count(table_in, table_out)

    print(count)
