import configparser
import os


class ReadConfig:
    """定义一个读取配置文件的类"""

    def __init__(self, filepath=None):
        if filepath:
            configpath = filepath
        else:
            #root_dir = os.path.dirname(os.path.abspath('.'))
            root_dir = os.path.abspath('.')
            configpath = os.path.join(root_dir, "config.ini")
            #print(configpath)
        self.cf = configparser.ConfigParser()
        self.cf.read(configpath)

    def get_db(self, section, option):
        value = self.cf.get(section, option)
        return value


if __name__ == '__main__':
    test = ReadConfig()
    t = test.get_db("ORACLE_DB", "conn_str")
    print(t)
    t = test.get_db("HTTP", "conn_str")
    print(t)

