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

DEF_LIWU_SPEED_STAT_PERIOD = 3
GIFT_SORTLIST_UPDATE=15

class LiwuStat(HYClass):
    def __init__(self, room_ctrl):
        HYClass.__init__(self, "DMSTAT")

        self.dbg_flag_add("DMSTAT", 0)

        self.room_ctrl = room_ctrl

        self.liwu_total = 0
        self.prev_liwu_total = 0
        self.liwu_speed_records = []
        self.stime = None
        self.etime = None
        self.liwu_monitor_state = 0

        self.prev_liwu_speed = 0
        self.liwu_speed_aver = 0
        self.monitor_period = DEF_LIWU_SPEED_STAT_PERIOD
        self.user_liwu={}
        self.result={}
        self.user_info={}
        self.records=[]
        self.other_records=[]

        self.room_ctrl.hdlr_add("gift", self.liwu_stat_recv_hdlr)
        self.room_ctrl.hdlr_add("char", self.char_stat_recv_hdlr)

        # {uid:{'values':1,txt:{dteventtime:"a"}}}

    def char_stat_recv_hdlr(self,data):
        #result={uid:{'values':num,'rank':num,'nn':str,'level':num}}
        if data['uid'] in self.result.keys():
            #self.result[data['uid']].setdefault('txt',{})
            #self.result[data['uid']]['txt'][data['time']]=data['txt']
            self.records.append({'type':data['type'],'time':data['time'],'uid':data['uid'],'txt':data['txt']})


    def liwu_sort_hdlr(self,delay): #排名前十的用户信息
        #tmp={(uid,int)}
        #result={uid:{'values':num,'rank':num}}
        while True:
            if len(self.user_liwu) <11:
                self.result={}
                tmp = sorted(self.user_liwu.iteritems(), key=lambda asd: asd[1], reverse=True)
                for i in range(0,len(tmp)):
                    self.result[tmp[i][0]] = {'values': tmp[i][1], 'rank': i}
            else:
                self.result={}
                tmp=sorted(self.user_liwu.iteritems(), key=lambda asd: asd[1],reverse=True)
                for i in range(0,10):
                    self.result[tmp[i][0]] = {'values': tmp[i][1], 'rank': i}


            '''result={uid:{'values':num,'rank':num,'nn':str,'level':num}}
                给result中添加昵称和等级字段
            '''
            for keyi,value in self.user_info.items():
                for keyj in self.result.keys():
                    if keyi==keyj:
                        self.result[keyj]['nn'] = value['nn']
                        self.result[keyj]['level'] = value['level']

            time.sleep(delay)


    # data = {'userid': STR, 'nickname': STR, 'level': INT, 'gift': STR, 'numb': INT }
    def liwu_stat_recv_hdlr(self, data):
        gift = self.room_ctrl.gift_get(data['gid'])
        if gift == None:
            self.dbg_err("DMSTAT", "Unkown gift %s" %(data['gid']))
            self.cnt_inc("unkown_gift")
            return False

        numb  = data['numb']
        self.liwu_total += gift['value'] * numb

        self.user_info[data['uid']]={
            'nn':data['nickname'],
            'level':data['level']}

        #保存用户ID和礼物总价值
        if data['uid'] in self.user_liwu.keys():
            self.user_liwu[data['uid']] += gift['value']* numb
        else:
            self.user_liwu[data['uid']] = gift['value'] * numb

        #保存礼物信息
        if data['uid'] in self.result.keys():
            self.records.append({'type':data['type'],'gname':data['gname'],'time':data['time'],'uid':data['uid']})

        else:
            self.other_records.append({'type':data['type'],'gname':data['gname'],'time':data['time'],'uid':data['uid']})



    def liwu_perv_speed_get(self):
        return self.prev_liwu_speed

    def liwu_speed_monitor(self):
        self.stime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())
        self.etime = "now"

        while (self.liwu_monitor_state):
            time.sleep(self.monitor_period)
            total = self.liwu_total
            speed = total - self.prev_liwu_total
            self.prev_liwu_speed = speed
            self.liwu_speed_records.append(speed)
            self.prev_liwu_total = total
            self.liwu_speed_aver = total / len(self.liwu_speed_records)

        self.etime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())

    def liwu_stat_start(self):
        if self.liwu_monitor_state:
            return True

        self.liwu_monitor_state = 1
        thread.start_new_thread(self.liwu_speed_monitor, ())
        thread.start_new_thread(self.liwu_sort_hdlr, (GIFT_SORTLIST_UPDATE,)) #礼物的排行刷新

        return True

    def liwu_stat_stop(self):
        self.liwu_monitor_state = 0
        return True


    def liwu_monitor_start(self):
        pass

    def liwu_monitor_stop(self):
        pass

    def help_liwu_stat_start(self):
        print    "   liwu_stat_start"
        print    "			 ----	开始统计礼物"

    def do_liwu_stat_start(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_liwu_stat_start()
            return

        self.liwu_stat_start()

    def help_liwu_stat_stop(self):
        print    "   liwu_stat_stop"
        print    "			 ----	停止统计礼物"

    def do_liwu_stat_stop(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_liwu_stat_stop()
            return

        self.liwu_stat_stop()

    def help_liwu_stat_info(self):
        print    "   liwu_stat_info"
        print    "			 ----	显示礼物统计信息"

    def do_liwu_stat_info(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_liwu_stat_stop()
            return

        print "  %s : %s -> %s" % (self.liwu_monitor_state, self.stime, self.etime)

        print "    liwu_total: ", self.liwu_total
        print "    prev_liwu_total:", self.prev_liwu_total

        print "    prev_liwu_speed:", self.prev_liwu_speed
        print "    liwu_speed_aver:", self.liwu_speed_aver
        print "    monitor_period:", self.monitor_period
        print "    liwu_speed_records:", len(self.liwu_speed_records)

        print "   ", self.liwu_speed_records

if __name__ == '__main__':
    room_ctrl = ZBRoom("ZBRM")
    stat = liwuStat(room_ctrl)
    stat.cmdloop()
