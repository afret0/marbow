# -*- coding: utf-8 -*-
import sys
import thread
import time
import logging
import uuid
import hashlib
import requests
import re

import os
import stat
import re
import requests
import ConfigParser
import random
import md5

from urllib import unquote

sys.path.append("..")

from hylib.hyclass import *

from client import *
from utils import *
from msger import *
from message import *


DOUYU_DOMAIN = 'www.douyu.com'


class Char(HYClass):
    def __init__(self, modid):
        self.modid = modid
        self.rid = 0
        self.ctrl_msger = Msger("CMER")
        self.data_msger = Msger("DMER")

        HYClass.__init__(self, "CHAR")

        self.dbg_flag_add("CHAR", 1)

    def get_ctrl_serv_list(self, rid):
        header = {
            'Host': "www.douyu.com",
            'Referer': "http://www.douyu.com/",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        }

        ret = []
        search_url = 'https://www.douyu.com/%s' % (rid)

        self.dbg_verb("CHAR", "CTRL server url %s " % (search_url))

        try:
            r = requests.get(search_url, headers=header)
        except:
            return ret

        auth_server_json = re.search('\$ROOM\.args\s=\s({.*});', r.text).group(1)

        try:
            server_json = json.loads(auth_server_json)['server_config']
            ret = json.loads(unquote(server_json))
        except:
            return ret

        return ret

    def ctrl_msgrepeaterlist_hdlr(self, msg):
        rstr = msg.attr('list')
        server = deserialize2(rstr)

        num = len(server)
        sid = random.randint(0, (num - 1))

        for i in range(0, num):
            self.dbg_verb("CHAR", "DATA server %.2d %s:%s" % (i, server[i]['ip'], server[i]['port']))

        host = server[sid]['ip']
        port = int(server[sid]['port'])

        self.dbg_noti("CHAR", "%d DATA server found, select %d." % (num, sid))
        self.data_msger.start(host, port, self.rid, self.ctrl_msger.uid_get())

        self.cnt_inc("ctrl_msgrepeaterlist_hdlr")

    def ctrl_setmsggroup_hdlr(self, msg):
        gid = msg.attr("gid")
        self.data_msger.gid_set(gid)
        self.cnt_inc("setmsggroup_hdlr")

    def ctrl_register(self, type, hdlr):
        self.ctrl_msger.msg_regiseter(type, hdlr)

    def data_register(self, type, hdlr):
        self.data_msger.msg_regiseter(type, hdlr)

    def char_enter(self, rid):

        self.rid = rid
        self.ctrl_msger.msg_regiseter('setmsggroup', self.ctrl_setmsggroup_hdlr)
        self.ctrl_msger.msg_regiseter('msgrepeaterlist', self.ctrl_msgrepeaterlist_hdlr)
        server = self.get_ctrl_serv_list(rid)

        num = len(server)
        sid = random.randint(0, (num - 1))

        for i in range(0, num):
            self.dbg_verb("CHAR", "CTRL server %.2d %s:%s" % (i, server[i]['ip'], server[i]['port']))

        self.dbg_noti("CHAR", "%d CTRL server found, select %d." % (num, sid))

        host = server[sid]['ip']
        port = int(server[sid]['port'])

        self.ctrl_msger.start(host, port, rid, None)  #ctrl_msger是Mesger对象

        time.sleep(2)
        self.dbg_noti("CHAR", "Has enter to room %s\n" % (self.rid))

    def char_exit(self):
        self.msgsend(u"marbow先走一步了，大家再见 ")
        self.ctrl_msger.stop()
        self.data_msger.stop()

        self.dbg_noti("CHAR", "Exit from room %s!" % (self.rid))
        self.rid = 0

    def msgsend(self, msg):
        self.ctrl_msger.sendmsg(msg)

    # 进入某个房间
    def help_enter(self):
        print    "	 enter ROOM_ID"
        print    u"			 ----	进入房间"

    def do_enter(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 1:
            self.help_enter()

        self.char_enter(argv[0])

    # 退出某个房间
    def help_exit(self):
        print    "	 exit"
        print    u"			 ----	退出房间 "

    def do_exit(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_exit()

        self.char_exit()

    # cookie
    def help_cookie(self):
        print    "   cookie [FILE]"
        print    u"			 ----	显示将COOKIE保存到文件"

    def do_cookie(self, line):
        argv = line.split()
        argc = len(argv)

        if argc > 1:
            self.help_cookie()

        cookies = get_chrome_cookies(DOUYU_DOMAIN)

        for key in cookies:
            print "%25s: %s" % (key, cookies[key])

        if argc == 1:
            json.dump(cookies, open(argv[0], 'w'))


# End Char
if __name__ == '__main__':
    char = Char("CHAR")
    char.cmdloop()

# End of file
