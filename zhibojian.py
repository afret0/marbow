#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from hylib.hyclass import *
from douyu.room import *
from danmu import *
from liwu import *
from shuiyou import *
from rengqi_stat import *
from guanzhu_stat import *

class Zhibojian(HYClass):
    def __init__(self, platform, rid):
        HYClass.__init__(self, "ZBJ")
        self.dbg_flag_add("ZBJ", 1)

        self.room_ctrl = self.create_room_ctrl(platform, rid)
        self.danmu_ctrl = Danmu(self.room_ctrl)
        self.liwu_ctrl = Liwu(self.room_ctrl)
        self.shuiyou_ctrl = Shuiyou(self.room_ctrl)
        self.renqi_ctrl=RenqiStat(self.room_ctrl)
        self.guanzhu_ctrl = GuanzhuStat(self.room_ctrl)
        self.rid=rid
        self.state='stop'


    def create_room_ctrl(self, platform, rid):
        if platform == None:
            return None
        elif platform == "douyu":
            return DouyuRoom(rid)
        else:
            return None

    def start(self):
        if self.state == "stop":
            self.state = "running"
            self.danmu_ctrl.danmu_start()
            self.liwu_ctrl.liwu_start()
            self.shuiyou_ctrl.suiyou_start()
            self.renqi_ctrl.renqi_stat_start()
            self.guanzhu_ctrl.guanzhu_stat_start()

            self.room_ctrl.start()

            self.stime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())
            self.etime  = "NOW"
            self.dbg_noti("ZBJ", "Zhibojian %s start." % (self.rid))

        return True

    def stop(self):
        if self.state == "running":
            self.room_ctrl.stop()
            self.danmu_ctrl.stop()
            self.liwu_ctrl.stop()
            self.shuiyou_ctrl.stop()

            self.state = "stop"
            self.etime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())
            self.dbg_noti("ZBJ", "Zhibojian %s stop." % (self.rid))

        return

    def zhibojian_start(self, zhibojian):
        rt = zhibojian.start()

        if rt == True:
            print "直播间%s ..... 启动成功！" % (zhibojian.rid)
        else:
            print "直播间%s ..... 启动失败！" % (zhibojian.rid)

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
        print    "			 ----	停止监控状态"

    def do_stop(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_stop()

        self.stop()

    def help_status(self):
        print    "   status"
        print    "			 ----	停止监控状态"

    def do_status(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 0:
            self.help_status()

        print "RID: %s STATE %s." %(self.rid, self.state)
        print "  %s -> %s." % (self.stime, self.etime)



    def help_renqi(self):
        print    "   status"
        print    "			 ----	停止监控状态"

    def do_renqi(self, line):
        print self.renqi_ctrl.renqi_total

    def help_room(self):
        print    "   room"
        print    "			 ---- 进入room命令行模式"

    def do_room(self, line):
        argv = line.split()
        argc = len(argv)

        if argc > 1:
            self.help_room()
            return

        self.room_ctrl.prompt = 'ROOM(%s): ' %(self.room_ctrl.info['platform'])
        self.room_ctrl.cmdloop()

    def help_danmu(self):
        print    "   danmu"
        print    "			 ---- 进入弹幕命令行模式"

    def do_danmu(self, line):
        argv = line.split()
        argc = len(argv)

        if argc > 1:
            self.help_danmu()
            return

        self.danmu_ctrl.prompt = 'DANMU(%s): ' %(self.rid)
        self.danmu_ctrl.cmdloop()

    def help_liwu(self):
        print    "   liwu"
        print    "			 ---- 进入liwu命令行模式"

    def do_liwu(self, line):
        argv = line.split()
        argc = len(argv)

        if argc > 1:
            self.help_liwu()
            return

        self.liwu_ctrl.prompt = 'LIWU(%s): ' %(self.rid)
        self.liwu_ctrl.cmdloop()

if __name__	== "__main__":
    zbj = Zhibojian("douyu", "846805")
    zbj.cmdloop()


