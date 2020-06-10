# coding=utf-8
from http_client import *#HttpClient
from data_oracle import *#DataOracle
from oracle_helper import *


import time
import sys


def main():

    timeTemp = time.time()
    #debug_drgs = ''
    debug_id = ''

    try:
        print("DRGs入组程序")
        # 1. 生成输入数据
        data_orc = DataOracle()

        test = readconfig.ReadConfig()
        fetch_count = int(test.get_db("ORACLE_DB", "fetch_count"))

        table_in = get_table_in()
        table_out = get_table_out()

        if fetch_count <= 0:
            print("fetch_count is error:", fetch_count)
            return

        print("一次获取数据条数：",fetch_count)

        print("统计总病例数...")
        count = data_orc.query_count(table_in, table_out)

        print("总例数为：", count)

        if count == 0:
            print("完毕")
            #input()
            return

        sqlMsg = '''  select
                         main_diag_code DISEASE_CODE,
                         AGE,
                         decode(trim(SEX),'1','男', '2','女', '9','其他') GENDER,
                         IN_DAYS ACCTUAL_DAYS,
                         hos_amount TOTAL_EXPENSE,
                         base_id B_WT4_V1_ID,
                         BABY_AGE       SF0100,
                         BABY_WEIGHT    SF0101,
                         BABY_IN_WEIGHT    SF0102,
                         trim(PAT_OUT_METHOD) SF0108,
                         other_diags_code DIAGS_OTHER,
                         other_oper_code OPERS
                         from %s t1
                         where not exists(select 1 from %s t2 where t2.base_id = t1.base_id)
                         and t1.main_diag_code is not null
                          ''' % (table_in, table_out)

        with OracleHelper() as oracle_h:
            oracle_h.execute_query(sqlMsg)

            print("开始病例入组...")

            results = oracle_h.fetchmany(fetch_count)



            n = 0
            while results:
                listParams = []

                for result in results:
                    # print(result)
                    listDiags = list(filter(None, str(result[10]).split(',')))
                    listOpers = list(filter(None, str(result[11]).split(',')))

                    hc = HttpClient()
                    hc.set_param1(result[0], result[1], result[2], result[3], result[4])
                    hc.set_param2(n, result[6], result[7], result[8],result[9])
                    hc.set_param3(listDiags, listOpers)
                    # print(result)

                    ret = hc.http_request()

                    ret_utf8 = ret.read().decode("utf-8")

                    #debug_drgs = ret_utf8

                    hc.http_close()


                    dic_ret_utf8 = json.loads(ret_utf8)
                    # print(dic_ret_utf8,'dic_ret_utf8')
                    # print(dic_ret_utf8['error'],'--------------dic_ret_utf8')
                    if len(dic_ret_utf8['drg']) == 3 or dic_ret_utf8['drg'] == '0000' or dic_ret_utf8['drg'] == '9999':
                        dic_ret_utf8['error'] = 'false'
                    else:
                        dic_ret_utf8['error'] = 'true'
                    dic_ret_utf8['pccl'] = ''

                    base_id = result[5] #dic_ret_utf8["B_WT4_V1_ID"]
                    debug_id = base_id

                    #设置插入条件
                    listP = []
                    listP.append(base_id),
                    #listP.append('');   #
                    listP.append(str(dic_ret_utf8["error"]))
                    listP.append(",".join(dic_ret_utf8["mdcs_main"]))
                    listP.append(','.join(dic_ret_utf8['adrgs_main']))#dic_ret_utf8['adrgs_main'])

                    listP.append(dic_ret_utf8["drg"])
                    listP.append(dic_ret_utf8['pccl'])
                    listP.append(dic_ret_utf8["oper_code"])
                    listP.append(dic_ret_utf8["error_log"])
                    listP.append(dic_ret_utf8["log"])
                    listParams.append(listP)
                # for i in listParams:
                #     print(i,"listParams--------")
                # print(len(listParams))
                    n += 1

                sqlInsertMsg = ''' insert into %s
                            (base_id, is_enter_group, mdc_code, adrg_code, drg_code, pccl, oper_code, error_log, log) 
                            values
                            
                            (:B_WT4_V1_ID, :error, :mdcs_main, :adrgs_main, :drg, :pccl, :oper_code, :error_log, :log)                           
                             ''' % (table_out)


                #print(listParams)
                listTuple = [tuple(i) for i in listParams]

                # for i in listTuple:
                #     print(i,'listTuple----')

                with OracleHelper() as oracle_insert:
                    oracle_insert.execute_sql_many(sqlInsertMsg, listParams)

                print(n, "/", count, "=", n / count * 100, "%")

                results = oracle_h.fetchmany(fetch_count)

        print("入组完毕", time.time() - timeTemp)
    except:
        print('出现异常:', sys.exc_info()[0])
        print('base_id:', debug_id)
        print( '当前时间：', time.asctime(time.localtime(time.time())),'；间隔时间：' ,time.time() - timeTemp)
    #input()


if __name__ == '__main__':
    try:
        main()
    except:
        print('main: error')