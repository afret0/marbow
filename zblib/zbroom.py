#-*- coding: utf-8 -*-

import sys
sys.path.append("..")
from hylib.hyclass import *
import json
import thread
from liwu_stat import *

DEF_STAT_PERIOD = 3
DEF_UPDATE_PERIOD = 1

class ZBRoom(HYClass):
    def __init__(self, modid):
        HYClass.__init__(self, modid)

        self.info  = {
            "platform":"",
            "roomid":"",
            "userid":"",
            "nickname":"",
            "passwd":"",
            "zhubo":"",
            "title":"",
            "ontime":"",
            "offtime":"",
            "block":"",
            "fans":0,
            "audience":0,
            "login":False,
            "follow":False,
            "tick":0,
            "update_period": DEF_UPDATE_PERIOD,
            "update": "UNINIT",
            "state": "UNINIT"
        }

        self.hdlr_tab = {
            'char':[self.def_char_hdlr],
            "gift":[self.def_gift_hdlr],
            "noti":[self.def_noti_hdlr],
            'uenter':[self.def_user_hdlr]
        }

        '''
       {"gid" ：492, "name" ："狗尾巴草", "value" : 1, "img" ："http://staticlive.douyucdn.cn/upload/dygift/1612/1124b301fdb5ad80836cea68fad33b''11.png”}
       '''

        self.gift_list = []
        self.info['update'] = "INIT"


    def def_user_hdlr(self,data):
        pass


    def status_update(self):
        while (self.info['update'] != "STOP"):
            self.info['update'] = "UPDATING"
            self.update()
            time.sleep(self.info['update_period'])

        self.info['update'] = "STOPED"


    def start(self):
        thread.start_new_thread(self.status_update, ())
        self.login()

    def stop(self):
        self.loglout()
        self.info['update'] = "STOP"

    def info_get(self):
        return self.info

    def hdlr_add(self, type, fun):
        hdlr_list = self.hdlr_tab[type]
        hdlr_list.append(fun)

    def hdlr_call(self, type, argv):
        hdlr_list = self.hdlr_tab[type] #相当于swithch开关，什么type调用什么函数

        for hdlr in hdlr_list: #函数调用
            rv = hdlr(argv)

            self.cnt_inc("self.hdlr_call")

            if rv == True:
                self.cnt_inc("self.hdlr_call_success")
            else:
                self.cnt_inc("self.hdlr_call_fail")

    # data = {'userid': STR, 'nickname': STR, 'level': INT, 'gift': STR, 'numb': INT }


#   {"el": "", "rni": "0", "uid": "1116720", "nn": "", "level": "21", "ic": "", "type": "uenter", "rid": "1164160"}
    def def_char_hdlr(self, data):
        self.cnt_inc("self.def_char_hdlr")

    # data = {'userid': STR, 'nickname': STR, 'level': INT, 'gid': GID, 'numb': INT }
    def def_gift_hdlr(self, data):
        self.cnt_inc("self.def_gift_hdlr")
        for gift_info in self.gift_list:
            if gift_info['gid']==data['gid']:
                data['gname']=gift_info['name']



    # data = {'userid': STR, 'nickname': STR, 'level': INT, 'gid': INT, 'numb': INT }
    def def_noti_hdlr(self, data):
        self.cnt_inc("self.def_noti_hdlr")



    # 内部接口
    def gift_get(self, gid):
       for gift in self.gift_list:
           if gift['gid'] == gid:
               return gift
       return None

    def is_online(self):
        if self.info['state'] == "ONLINE":
            return True
        else:
            return False

    def online(self):
        if self.info['state'] != "ONLINE":
            self.info['state'] = "ONLINE"
            self.info['ontime'] = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())
            self.info['offtime'] = "now"

    def offline(self):
        if self.info['state'] != "OFFLINE":
            if self.info['state'] == "ONLINE":
                self.info['offtime'] = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())

            self.info['state'] = "OFFLINE"

    # 外部接口，各子类需要自己重构
    # 登录 data {"nicknamename": STR, "password":STR}
    def update(self):
        self.info['tick'] += 1
        return False

    def login(self):
        return False

    # 登出
    def loglout(self):
        return False

    # 发生弹幕 data {"type": STR,"txt": TXT}
    def char_send(self, data):
        cdata = {
            'nickname':self.info['nickname'],
            'level': 0,
            'txt':data['txt']
        }

        self.hdlr_call("char", cdata)

    # 赠送礼物 data {"name": STR， "number": INIT 服务·4}

    def gift_send(self, data):
        cdata = {
            'userid':  self.info['userid'],
            'nickname': self.info['nickname'],
            'level': 0,
            'gift': data['type'],
            'numb': data['numb']
        }

        self.hdlr_call("gift", cdata)

        return False

    # 赠送礼物 data {"name": STR， "number": INIT 服务·4}
    def noti_send(self, data):
        cdata = {
            'type': data['type'],
            'msg': data['msg']
        }

        self.hdlr_call("noti", cdata)

        return False

    # 关注
    def follow(self):
        return False

    # 取关
    def unfollow(self):
        return False

    # 现实已注册回调函数
    def help_hdlr(self):
        print    "   hdlr"
        print    "			 ----	显示所有的注册回调函数"

    def do_hdlr(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_hdlr()
            return

        for key, hdlr_list in self.hdlr_tab.items():
            numb = len(hdlr_list)

            print "  %d handler for \'%s\':" %(numb, key)

            for hdlr in hdlr_list:
                print "    ", hdlr.__name__

    # 获取房间信息
    def help_info(self):
        print    "   info"
        print    "			 ----	显示所有的注册回调函数"

    def do_info(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_info()
            return

        info = self.info_get()

        for key, value in info.items():
            print "%8s: %s" % (key, value)

        for gift in self.gift_list:

            print "  ================================================================================================="
            print "    gid   ： ", gift['gid']
            print "    name  ： ", gift['name']
            print "    value ： ", gift['value']
            print "    img   ： ", gift['img']

    # 修改房间状态为上线
    def help_online(self):
        print    "   online"
        print    "			 ----	将直播间设置为上线状态"

    def do_online(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_online()
            return

        self.online()

    # 修改房间状态为上线
    def help_offline(self):
        print    "   offline"
        print    "			 ----	将直播间设置为下线状态"

    def do_offline(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_offline()
            return

        self.offline()

    # 修改房间状态为上线
    def help_update(self):
        print    "   update"
        print    "			 ----	更新房间状态"

    def do_update(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_update()
            return

        self.update()

    # 修改房间状态为上线
    def help_char(self):
        print    "   char TYPE TXT"
        print    "			 ----	发生信息"

    def do_char(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 2:
            self.help_char()
            return

        type = argv[0]
        txt  = argv[1]

        data = {"type":type, "txt":txt}

        self.char_send(data)

    # 修改房间状态为上线
    def help_gift(self):
        print    "   gift TYPE NUMB"
        print    "			 ---- 赠送礼物"

    def do_gift(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 2:
            self.help_gift()
            return

        type = argv[0]
        numb = int(argv[1])

        data = {"type": type, "numb": numb}

        self.gift_send(data)

    # 修改房间状态为上线
    def help_noti(self):
        print    "   noti TYPE MSG RID NICKNAME LEVEL"
        print    "			 ---- 发送通告信息"

    def do_noti(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 2:
            self.help_noti()
            return

        type = argv[0]
        msg  = argv[1]

        data = {"type": type, "msg": msg}

        self.noti_send(data)

    # 修改房间状态为上线
    def help_user(self):
        print    "   user RID NICKNAME PWD LEVEL"
        print    "			 ---- 发送通告信息"

    def do_user(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 4:
            self.help_user()
            return

        self.info['rid']      = argv[0]
        self.info['nickname'] = argv[1]
        self.info['passwd']   = argv[2]
        self.info['level']    = argv[3]

    # 打印礼物列表

    def help_gift_type(self):
        print    "  gift_type"
        print    "			 ---- 打印礼物列表"

    def do_gift_type(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_gift_type()
            return

        for gift in value:
            print "    ID: %d, 名称: %s, 价值: %d" %(gift['gid'], gift['type'], gift['value'])

    def help_start(self):
        print    "   start [RID]"
        print    "			 ----	启动直播间"

    def do_start(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_start()

        self.start()

    def help_stop(self):
        print    "   stop"
        print    "			 ----	停止直播间"

    def do_stop(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_stop()

        self.stop()

# End of ZBRoom

if __name__ == '__main__':
    room = ZBRoom("ZBRM")
    room.cmdloop()
