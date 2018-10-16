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
from liwu_stat import *

DEF_DANMU_SPEED_STAT_PERIOD = DEF_STAT_PERIOD

class DanmuStat(HYClass):
    def __init__(self, room_ctrl):
        HYClass.__init__(self, "DMSTAT")

        self.dbg_flag_add("DMSTAT", 0)

        self.room_ctrl = room_ctrl

        self.danmu_total = 0
        self.prev_danmu_total = 0
        self.danmu_speed_records = []
        self.stime = None
        self.etime = None
        self.danmu_monitor_state = 0

        self.prev_danmu_speed = 0
        self.danmu_speed_aver = 0
        self.monitor_period = DEF_DANMU_SPEED_STAT_PERIOD
        self.uenter_info=[]

        self.room_ctrl.hdlr_add("char", self.danmu_stat_recv_hdlr)

        self.room_ctrl.hdlr_add("uenter", self.uenter_hdlr)


    def uenter_hdlr(self,data):
        if len(self.uenter_info):
            self.uenter_info.pop()
            self.uenter_info.append({'uid':data.body['uid'],
                                     'nn': data.body['nn'],
                                     'level': data.body['level']
                                     })
        else:
            self.uenter_info.append({'uid': data.body['uid'],
                                     'nn': data.body['nn'],
                                     'level': data.body['level']
                                     })


    def danmu_stat_recv_hdlr(self, data):
        self.danmu_total += 1


    def danmu_perv_speed_get(self):
        return self.prev_danmu_speed

    def danmu_speed_monitor(self):
        self.stime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())
        self.etime = "now"

        while (self.danmu_monitor_state):
            time.sleep(self.monitor_period)
            total = self.danmu_total
            speed = total - self.prev_danmu_total
            self.prev_danmu_speed = speed
            self.danmu_speed_records.append(speed)
            self.prev_danmu_total = total
            self.danmu_speed_aver = total / len(self.danmu_speed_records)

        self.etime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())

    def danmu_stat_start(self):
        if self.danmu_monitor_state:
            return True

        self.danmu_monitor_state = 1
        thread.start_new_thread(self.danmu_speed_monitor, ())

        return True

    def danmu_stat_stop(self):
        self.danmu_monitor_state = 0
        return True

    def help_danmu_stat_start(self):
        print    "   danmu_stat_start"
        print    "			 ----	开始统计弹幕"

    def do_danmu_stat_start(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_danmu_stat_start()
            return

        self.danmu_stat_start()

    def help_danmu_stat_stop(self):
        print    "   danmu_stat_stop"
        print    "			 ----	停止统计弹幕"

    def do_danmu_stat_stop(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_danmu_stat_stop()
            return

        self.danmu_stat_stop()

    def help_danmu_stat_info(self):
        print    "   danmu_stat_info"
        print    "			 ----	现实弹幕统计信息"

    def do_danmu_stat_info(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_danmu_stat_stop()
            return

        print "  %s : %s -> %s" % (self.danmu_monitor_state, self.stime, self.etime)

        print "    danmu_total: ", self.danmu_total
        print "    prev_danmu_total:", self.prev_danmu_total

        print "    prev_danmu_speed:", self.prev_danmu_speed
        print "    danmu_speed_aver:", self.danmu_speed_aver
        print "    monitor_period:", self.monitor_period
        print "    danmu_speed_records:", len(self.danmu_speed_records)

        print "   ", self.danmu_speed_records

if __name__ == '__main__':
    room_ctrl = ZBRoom("ZBRM")
    stat = DanmuStat(room_ctrl)
    stat.cmdloop()
