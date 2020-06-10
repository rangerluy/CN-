import http.client
import json
import readconfig


#strconn = "10.67.78.44:3001"

test = readconfig.ReadConfig()
strconn = test.get_db("HTTP", "conn_str")

data_src = {
        'DISEASE_CODE': 'A01.100y001',                              #主要诊断
        'AGE': 42,                                                     #年龄
        'GENDER': '女',                                                #性别（男、女）
        'ACCTUAL_DAYS': 6,
        'TOTAL_EXPENSE': 917.92,

        'B_WT4_V1_ID': '35294a211',                                 #病历首页的主键
        'SF0100':-1,                                                  #新生儿天数，缺失或不传为-1
        'SF0102':-1,                                                   #新生儿体重，缺失或不传为-1
        'SF0104':-1,                                                    #呼吸机使用时间，缺失或不传为-1
        'SF0108':1,                                                     #出院转归，缺失或不传为-1
        'diags_code': ["C90.001","Z94.802","D64.901","E77.801"],    #其他诊断
        'opers_code': []                                                #手术/操作
    }

class HttpClient:
    def __init__(self):
        self.__conn = http.client.HTTPConnection(strconn)
        self.__headers = {"Content-Type": "application/json"}
        self.__data = {
                'DISEASE_CODE': '',                              #主要诊断
                'AGE': 0,                                                     #年龄
                'GENDER': '',                                                #性别（男、女）
                'ACCTUAL_DAYS': 0,
                'TOTAL_EXPENSE': 0,
                'B_WT4_V1_ID': '',                                 #病历首页的主键

                'SF0100':-1,                                                  #新生儿天数，缺失或不传为-1
                'SF0101':-1,                                                   #新生儿出生体重
                'SF0102':-1,                                                   #新生儿入院体重，缺失或不传为-1
                'SF0104':-1,                                                    #呼吸机使用时间，缺失或不传为-1
                'SF0108':-1,                                                     #出院转归，缺失或不传为-1
                'diags_code': [],    #其他诊断
                'opers_code': []                                                #手术/操作
            }

    def set_param1(self,disease_code, age, gender, in_days, expense):
        self.__data['DISEASE_CODE'] = disease_code

        if age is None:
            self.__data['AGE'] = 0
        else:
            self.__data['AGE'] = int(age)

        self.__data['GENDER'] = gender
        self.__data['ACCTUAL_DAYS'] = in_days
        self.__data['TOTAL_EXPENSE'] = expense

    def set_param2(self,id, baby_age, baby_weight,baby_in_weight, out_method):
        self.__data['B_WT4_V1_ID'] = id

        b_age = baby_age
        if baby_age is None:
            b_age = -1

        self.__data['SF0100'] = b_age

        b_weight = baby_weight
        if baby_weight is None:
            b_weight = -1

        self.__data['SF0101'] = b_weight

        b_weight2 = baby_in_weight
        if baby_in_weight is None:
            b_weight2 = -1

        self.__data['SF0102'] = b_weight2
        #self.__data['SF0104'] = xx

        b_out_method = str(out_method).strip()
        if out_method is None:
            b_out_method = -1

        self.__data['SF0108'] = b_out_method

    def set_param3(self,diags_code, opers_code):
        self.__data['diags_code'] = diags_code
        self.__data['opers_code'] = opers_code

    def http_request(self):
        try:
            data = json.dumps(self.__data)
            #print(self.__data)
            #print(data)


            self.__conn.request("POST", '/comp_drg', data, self.__headers)
            res = self.__conn.getresponse()
        except:
            print('error func: http_request')
            print('error data:', self.__data)
        return res

    def http_close(self):
        self.__conn.close()


if __name__ == '__main__':
        # hc = HttpClient()
        # hc.set_param1('K85.900y001', 36, '其它', 7, 5184.87)
        #
        # hc.set_param2(28197, -1, -1, 1)
        #
        # hc.set_param3(['E11.900y001', 'E78.500y001', 'I10.x00x027', 'K76.000y001', 'K86.200y001'], [])
        #
        # ret = hc.http_request()
        # print(ret.read().decode("utf-8"))

        hc = HttpClient()
        hc.set_param1('I46.100x001', 30, '女', 7, 5184.87)

        hc.set_param2(28197, -1, -1, -1, 1)

        hc.set_param3([], [])

        ret = hc.http_request()
        print(ret.read().decode("utf-8"))


