#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import MySQLdb
import thread
from douyu.char import *
from danmu_talk import *
from zblib.zbroom import *


DEF_RENQI_SPEED_STAT_PERIOD = DEF_STAT_PERIOD

class RenqiStat(HYClass):
    def __init__(self, room_ctrl):
        HYClass.__init__(self, "DMSTAT")

        self.dbg_flag_add("DMSTAT", 0)

        self.room_ctrl = room_ctrl

        self.renqi_total = 0
        self.prev_renqi_total = 0
        self.renqi_records = []
        self.stime = None
        self.etime = None
        self.renqi_monitor_state = 0

        self.renqi_aver = 0
        self.monitor_period = DEF_RENQI_SPEED_STAT_PERIOD

    def renqi_perv_get(self):
        return self.prev_renqi_total

    def renqi_monitor(self):
        self.stime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())
        self.etime = "now"

        '''
                    time.sleep(self.monitor_period)
            total = self.liwu_total
            speed = total - self.prev_liwu_total
            self.prev_liwu_speed = speed
            self.liwu_speed_records.append(speed)
            self.prev_liwu_total = total
            self.liwu_speed_aver = total / len(self.liwu_speed_records)
        '''

        while (self.renqi_monitor_state):
            time.sleep(self.monitor_period)
            total = self.room_ctrl.info['audience']
            self.renqi_total=total
            self.renqi_records.append(total)
            self.prev_renqi_total = total
            self.renqi_aver = total / len(self.renqi_records)

        self.etime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())

    def renqi_stat_start(self):
        if self.renqi_monitor_state:
            return True

        self.renqi_monitor_state = 1
        thread.start_new_thread(self.renqi_monitor, ())

        return True

    def renqi_stat_stop(self):
        self.renqi_monitor_state = 0
        return True

    def help_renqi_stat_start(self):
        print    "   renqi_stat_start"
        print    "			 ----	开始统计人气"

    def do_renqi_stat_start(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_renqi_stat_start()
            return

        self.renqi_stat_start()

    def help_renqi_stat_stop(self):
        print    "   renqi_stat_stop"
        print    "			 ----	停止统计人气"

    def do_renqi_stat_stop(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_renqi_stat_stop()
            return

        self.renqi_stat_stop()

    def help_renqi_stat_info(self):
        print    "   renqi_stat_info"
        print    "			 ---- 显示人气统计信息"

    def do_renqi_stat_info(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_renqi_stat_stop()
            return

        print "  %s : %s -> %s" % (self.renqi_monitor_state, self.stime, self.etime)

        print "    renqi_total: ", self.renqi_total
        print "    prev_renqi_total:", self.prev_renqi_total

        print "    monitor_period:", self.monitor_period
        print "    renqi_records:", len(self.renqi_records)
        print "   ", self.renqi_records

if __name__ == '__main__':
    room_ctrl = ZBRoom("ZBRM")
    stat = RenqiStat(room_ctrl)
    stat.cmdloop()
