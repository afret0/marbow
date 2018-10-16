#-*- coding: utf-8 -*-

import sys
reload(sys);
sys.setdefaultencoding('utf-8');

import time
import MySQLdb
import thread
from douyu.char import *
from talk import *
from zblib.zbroom import *
from rengqi_stat import  *

DEF_LIWU_SPEED_STAT_PERIOD = DEF_STAT_PERIOD

class shuiyouStat(HYClass):
    def __init__(self, room_ctrl):
        HYClass.__init__(self, "DMSTAT")

        self.dbg_flag_add("DMSTAT", 0)

        self.room_ctrl = room_ctrl


        self.monitor_period = DEF_LIWU_SPEED_STAT_PERIOD

        self.room_ctrl.hdlr_add("char", self.shuiyou_danmu_recv_hdlr)
        self.room_ctrl.hdlr_add("gift", self.shuiyou_liwu_recv_hdlr)
        self.shuiyou_tab = {}

    #def shuiyou_

    # data = {'userid': STR, 'nickname': STR, 'level': INT, 'gift': STR, 'numb': INT }
    def shuiyou_danmu_recv_hdlr(self, data):
        name = data['nickname']
        value = self.room_ctrl.gift_value_get(type)

    # data = {'userid': STR, 'nickname': STR, 'level': INT, 'gift': STR, 'numb': INT }
    def shuiyou_gift_recv_hdlr(self, data):
        type = data['gift']
        value = self.room_ctrl.gift_value_get(type)

    def shuiyou_perv_speed_get(self):
        return self.prev_shuiyou_speed

    def shuiyou_speed_monitor(self):
        self.stime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())
        self.etime = "now"

        while (self.shuiyou_monitor_state):
            time.sleep(self.monitor_period)
            total = self.shuiyou_total
            speed = total - self.prev_shuiyou_total
            self.prev_shuiyou_speed = speed
            self.shuiyou_speed_records.append(speed)
            self.prev_shuiyou_total = total
            self.shuiyou_speed_aver = total / len(self.shuiyou_speed_records)

        self.etime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())

    def shuiyou_stat_start(self):
        if self.shuiyou_monitor_state:
            return True

        self.shuiyou_monitor_state = 1
        thread.start_new_thread(self.shuiyou_speed_monitor, ())

        return True

    def shuiyou_stat_stop(self):
        self.shuiyou_monitor_state = 0
        return True

    def help_shuiyou_stat_start(self):
        print    "   shuiyou_stat_start"
        print    "			 ----	开始统计礼物"

    def do_shuiyou_stat_start(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_shuiyou_stat_start()
            return

        self.shuiyou_stat_start()

    def help_shuiyou_stat_stop(self):
        print    "   shuiyou_stat_stop"
        print    "			 ----	停止统计礼物"

    def do_shuiyou_stat_stop(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_shuiyou_stat_stop()
            return

        self.shuiyou_stat_stop()

    def help_shuiyou_stat_info(self):
        print    "   shuiyou_stat_info"
        print    "			 ----	显示礼物统计信息"

    def do_shuiyou_stat_info(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_shuiyou_stat_stop()
            return

        print "  %s : %s -> %s" % (self.shuiyou_monitor_state, self.stime, self.etime)

        print "    shuiyou_total: ", self.shuiyou_total
        print "    prev_shuiyou_total:", self.prev_shuiyou_total

        print "    prev_shuiyou_speed:", self.prev_shuiyou_speed
        print "    shuiyou_speed_aver:", self.shuiyou_speed_aver
        print "    monitor_period:", self.monitor_period
        print "    shuiyou_speed_records:", len(self.shuiyou_speed_records)

        print "   ", self.shuiyou_speed_records

if __name__ == '__main__':
    room_ctrl = ZBRoom("ZBRM")
    stat = shuiyouStat(room_ctrl)
    stat.cmdloop()
