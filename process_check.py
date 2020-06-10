import win32com.client
import readconfig
import os
import time

def CheckProcExistByPN(process_name):
    try:
        WMI = win32com.client.GetObject('winmgmts:')
        processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    except Exception as e:
        print(process_name + "error : ", e)

    if len(processCodeCov) > 0:
        print(
        process_name + " exist")
        return 1
    else:
        print(
        process_name + " is not exist")
        return 0


if __name__ == '__main__':

    while True:
        test = readconfig.ReadConfig()
        exe_name = test.get_db("EXE", "file_name")
        exe_path = test.get_db('EXE', 'path')
        timeout = int(test.get_db('EXE', 'timeout'))

        print('监测时间：', timeout)

        file = exe_path+ '\\'+ exe_name

        print(file)

        if os.path.exists(file) is True:
            print('True')


        ret = CheckProcExistByPN(exe_name)

        if ret == 0:
            print('进程不存在，开启进程。。。')
            os.system(file)

        time.sleep(timeout)