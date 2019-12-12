import os
  # ----------------------自动拨号更换IP-----------------------------

class Get_Ip():

    def connect(self):
        name = "宽带连接"
        username = 'wzg.22576911'
        password = "542861"
        cmd_str = "rasdial %s %s %s" % (name, username, password)
        res = os.system(cmd_str)
        if res == 0:
            print("连接成功")
        else:
            print(res)

    def disconnect(self):
        name = "宽带连接"
        cmdstr = "rasdial %s /disconnect" % name
        os.system(cmdstr)
        print('断开成功')

    def huan_ip(self):
        # 断开网络
        self.disconnect()
        # 开始拨号
        self.connect()

