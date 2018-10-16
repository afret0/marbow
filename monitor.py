#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import thread
from time import *

from douyu.room import *
from database import *

DEF_MON_PERIOD=60

ROOM_TABLE = "room"

class Monitor(Database):
    def __init__(self, modid):
        self.room_id_list = []
        self.room_list=[]
        self.state = False
        self.period = DEF_MON_PERIOD
        
        Database.__init__(self, modid)

    def room_record(self, rid):
        """
        ret = {
               "room_id"        : data['room_id'],
               'room_thumb'     : data['room_thumb'],
               "cate_id"        : data['cate_id'],
               "cate_name"      : data['cate_name'],
               "room_name"      : data['room_name'],
               "room_status"    : data['room_status'],
               "owner_name"     : data['owner_name'],
               "avatar"         : data['avatar'],
               "online"         : data['online'],
               "owner_weight"   : data['owner_weight'],
               "fans_num"       : data['fans_num'],
               "start_time"     : data['start_time']
            }
        """
        info = self.get_info(rid)
        if data['room_status'] == 0:
            return

        tstr = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())
        sql = 'INSERT INTO %s (time, rid, online, fans) VALUES("%s", %s, %s, %s);'  % (ROOM_TABLE, tstr, info['room_id'], info['online'], info['fans_num'])
        self.db_submit(sql)


    def mon_start(self):
        if self.state != 0:
            return

        self.state = 2

        while self.state  == 2:
            num = len(self.room_id_list)

            for i in range(0, num):
                self.room_record(self.room_id_list[i])

            sleep(self.period)

        self.state = 0

        thread.exit_thread()

    def mon_stop(self):
        self.state = 1

    def room_add(self, rid):
        self.room_id_list.append(rid)

    def room_del(self, rid):
        self.room_id_list.remove(rid)

    # 获取房间信息
    def help_monitor_add(self):
        print    "   monitor_add ROOMID"
        print    "			 ----	添加监控直播间"

    def do_monitor_add(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 1:
            self.help_monitor_add()

        rid = argv[0]

        self.room_add(rid)

    # 获取房间信息
    def help_monitor_del(self):
        print    "   monitor_del ROOMID"
        print    "			 ----	移除监控直播间"

    def do_monitor_del(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 1:
            self.help_monitor_del()

        rid = argv[0]

        self.room_del(rid)

    # 获取房间信息
    def help_monitor(self):
        print    "   monitor"
        print    "			 ----	现实监控状态"

    def do_monitor(self, line):
        argv = line.split()
        argc = len(argv)

        if argc !=0:
            self.help_monitor()

        if self.state == 2:
            print "运行中..."
        elif self.state == 1:
            print "关闭中..."
        else:
            print "已关闭！"

        num = len(self.room_id_list)

        print "监控周期为%d秒，%d个直播间被监控：" %(self.period, num)

        for i in range(0, num):
            print "  %d : %s" %(i, self.room_id_list[i])

    # 启动监控
    def help_monitor_start(self):
        print    "   monitor_start"
        print    "			 ----	现实监控状态"

    def do_monitor_start(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_monitor_start()

        if self.state == 2:
            print "监控运行中，将不会重新启动"
        elif self.state == 1:
            print "监控关闭中，将被重新启动"
            self.state = 2
        else:
            thread.start_new_thread(self.mon_start(), ())
            print "监控启动成功."

    # 停止监控
    def help_monitor_stop(self):
        print    "   monitor_stop"
        print    "			 ----	停止监控状态"

    def do_monitor_stop(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_monitor_stop()

        self.mon_stop()

        print "已通知线程关闭，请稍后检测监控状态"

# End of Monitor

if __name__ == '__main__':
    monitor = Monitor("MON")
    monitor.cmdloop()