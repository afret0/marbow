#-*- coding: utf-8 -*-

import sys
reload(sys);
sys.setdefaultencoding('utf-8');

import time
import MySQLdb
import thread
from douyu.char import *
from danmu_talk import *
from zblib.zbroom import *

DEF_GUANZHU_SPEED_STAT_PERIOD = DEF_STAT_PERIOD

class GuanzhuStat(HYClass):
    def __init__(self, room_ctrl):
        HYClass.__init__(self, "DMSTAT")

        self.dbg_flag_add("DMSTAT", 0)

        self.room_ctrl = room_ctrl

        self.guanzhu_total = 0
        self.prev_guanzhu_total = 0
        self.guanzhu_speed_records = []
        self.stime = None
        self.etime = None
        self.guanzhu_monitor_state = 0

        self.prev_guanzhu_speed = 0
        self.guanzhu_speed_aver = 0
        self.monitor_period = DEF_GUANZHU_SPEED_STAT_PERIOD



    def guanzhu_perv_speed_get(self):
        return self.prev_guanzhu_speed

    def guanzhu_speed_monitor(self):
        self.stime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())
        self.etime = "now"

        while (self.guanzhu_monitor_state):
            time.sleep(self.monitor_period)
            total = self.room_ctrl.info['fans']
            self.guanzhu_total=total
            self.guanzhu_speed_records.append(total)
            self.prev_guanzhu_total = total
            self.guanzhu_aver =int(total) / len(self.guanzhu_speed_records)

        self.etime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())

    def guanzhu_stat_start(self):
        if self.guanzhu_monitor_state:
            return True

        self.guanzhu_monitor_state = 1
        thread.start_new_thread(self.guanzhu_speed_monitor, ())

        return True

    def guanzhu_stat_stop(self):
        self.guanzhu_monitor_state = 0
        return True

    def help_guanzhu_stat_start(self):
        print    "   guanzhu_stat_start"
        print    "			 ----	开始统计关注"

    def do_guanzhu_stat_start(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_guanzhu_stat_start()
            return

        self.guanzhu_stat_start()

    def help_guanzhu_stat_stop(self):
        print    "   guanzhu_stat_stop"
        print    "			 ----	停止统计关注"

    def do_guanzhu_stat_stop(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_guanzhu_stat_stop()
            return

        self.guanzhu_stat_stop()

    def help_guanzhu_stat_info(self):
        print    "   guanzhu_stat_info"
        print    "			 ----	查看关注统计信息"

    def do_guanzhu_stat_info(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_guanzhu_stat_stop()
            return

        print "  %s : %s -> %s" % (self.guanzhu_monitor_state, self.stime, self.etime)

        print "    guanzhu_total: ", self.guanzhu_total
        print "    prev_guanzhu_total:", self.prev_guanzhu_total

        print "    prev_guanzhu_speed:", self.prev_guanzhu_speed
        print "    guanzhu_speed_aver:", self.guanzhu_speed_aver
        print "    monitor_period:", self.monitor_period
        print "    guanzhu_speed_records:", len(self.guanzhu_speed_records)

        print "   ", self.guanzhu_speed_records

if __name__ == '__main__':
    room_ctrl = ZBRoom("ZBRM")
    stat = GuanzhuStat(room_ctrl)
    stat.cmdloop()
