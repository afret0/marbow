#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from database import *

ZB_TABLE="zhubo"

class Zhubo(Database):
    def __init__(self, modid):
        self.modid = modid
        Database.__init__(self, modid)
        self.dbg_flag_add("ZB", 1)

    def zb_nn2id(self, nn):
        sql = 'SELECT idx FROM %s WHERE alias LIKE "%%%s%%";' % (ZB_TABLE, nn)
        results = self.db_select(sql)

        if results:
            idxs = results[0:][0]
            return idxs
        else:
            return None

    def zb_info_get(self, idx):
        sql = 'SELECT idx FROM %s WHERE alias=%d' % (ZB_TABLE, idx)
        results = self.db_select(sql)

        if results:
            idxs = results[0:][0]
            return idxs
        else:
            return None

    # 从数据库中存取会话
    def help_nn2id(self):
        print    "	 nn2id NICKNAME"
        print    u"			 ---- 根据别名查找主播ID "

    def do_nn2id(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 1:
            self.help_nn2id()
            return
        nn = argv[0]
        idxs = self.zb_nn2id(nn)

        if idxs:
            num = len(idxs)
            print u"找到%d个答案:" % (num)
            for i in range(0, num):
                idx = idxs[i]
                print u"  %.2d: %s" % (i, idx)
        else:
            print u"没有此昵称！"

            # 从数据库中存取会话

    def help_zbinfo(self):
        print    "	 zbinfo NICKNAME"
        print    u"			 ---- 显示主播的资料 "

    def do_zbinfo(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 1:
            self.help_nn2id()
            return
        nn = argv[0]
        idxs = self.zb_nn2id(nn)

        if idxs:
            num = len(idxs)
            print u"找到%d个答案:" % (num)
            for i in range(0, num):
                idx = idxs[i]
                print u"  %.2d: %s" % (i, idx)
        else:
            print u"没有此昵称！"

if __name__	== "__main__":
    zb = Zhubo("ZB")
    zb.cmdloop()