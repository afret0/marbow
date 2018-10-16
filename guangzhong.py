# -*- coding: utf-8 -*-

import sys

reload(sys);
sys.setdefaultencoding('utf-8');

import time
import MySQLdb
import thread
from douyu.char import *
from talk import *
from rengqi_stat import *
from guanzhu_stat import *
from shuiyou_stat import *


class Guangzhong(RengqiStat, GuanzhuStat, ShuiyouStat):
    def __init__(self, room_ctrl):
        self.room_ctrl = room_ctrl

        RenqiStat.__init__(self, room_ctrl)
        GuanzhuStat.__init__(self, room_ctrl)
        ShuiyouStat.__init__(self, room_ctrl)

    def guangzhong_start(self):
        self.stat_start()

    def guangzhong_stop(self):
        self.stat_stop()

    # 监控弹幕
    def help_guangzhong_monitor(self):
        print    "   guangzhong_monitor [start|stop]"
        print    u"			 ----	发送弹幕"

    def do_guangzhong_monitor(self, line):
        argv = line.split()
        argc = len(argv)

        if argc > 1:
            self.help_guangzhong()
            return

        if argc == 0:
            print "guangzhong_monitor_state: ", self.guangzhong_monitor_state
        else:
            if argv[0] == "start":
                self.guangzhong_monitor_start()
            elif argv[0] == "stop":
                self.guangzhong_monitor_stop()
            else:
                self.help_guangzhong()
                return


# End of Guangzhong

if __name__ == '__main__':
    guangzhong = Guangzhong("GUANGZHONG")
    guangzhong.cmdloop()
# End of file
