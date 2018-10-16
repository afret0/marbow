#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re

from database import *
from tuling import *

from zblib.zbroom import *

class DanmuTalk(Tuling, Database):
    def __init__(self, room_ctrl):
        self.modid = "DMTALK"
        Tuling.__init__(self, "TULI")
        Database.__init__(self, "DB")

        self.dbg_flag_add("DMTALK", 1)
        self.dbg_flag_add("ANSDB", 0)

        self.room_ctrl = room_ctrl

        self.room_ctrl.hdlr_add("char", self.danmu_talk_recv_hdlr)

    def danmu_talk_recv_hdlr(self, data):
        self.cnt_inc("danmu_recv_hdlr")
        self.talk(data)

    def question_fetch(self, txt):
        try:
            npos = txt.index("marbow")

            q = txt[npos + len("marbow"):]

            q = re.sub(u"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", q)
            q = re.sub(u" ", "", q)

            return q
        except:
            self.cnt_inc("question_fetch_except")
            return None

    def ask(self, question):

        if self.dbg_flag_vaild("ANSDB"):
            answer = self.db_answer_lookup(question)

            if answer:
                self.cnt_inc("danmu_local")
            else:
                answer = self.tuling_answer_lookup(question)
                self.cnt_inc("danmu_tuling")
                self.db_answer_add(question, answer)
        else:
            answer = self.tuling_answer_lookup(question)
            self.cnt_inc("danmu_tuling")

        return answer

    def talk(self, rdata):
        nn    = rdata['nn']
        level = rdata['level']
        txt   = rdata['txt']

        if nn == "marbow":
            self.cnt_inc("danmu_self")
            return

        question = self.question_fetch(txt)

        if question == None:
            self.cnt_inc("danmu_other")
            return

        self.cnt_inc("ask")
        # 现在本地数据库查找答案
        answer = self.ask(question)

        stxt = "@%s, %s" % (nn, answer)

        sdata = {"type":"normal", "txt":stxt}

        self.room_ctrl.char_send(sdata)

        self.cnt_inc("answer")

    def talk_start(self):
        pass


    def talk_stop(self):
        pass

    def help_danmu_talk(self):
        print    "	 danmu_talk QUESTION"
        print    u"			 ----	与marbow对话"

    def do_danmu_talk(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 1:
            self.help_danmu_talk()
            return

        question = argv[0]
        data = {'nn':"tester", "level":"0", "txt":question}
        self.talk(data)

# End of Talk

if __name__ == '__main__':
    room_ctrl = ZBRoom("ZBRM")
    talk = DanmuTalk(room_ctrl)
    talk.cmdloop()

# End of file