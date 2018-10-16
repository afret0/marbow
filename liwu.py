#-*- coding: utf-8 -*-

import sys
reload(sys);
sys.setdefaultencoding('utf-8');

import time
import MySQLdb
import thread
from douyu.char import *
from danmu_talk import *
from liwu_stat import *

class Liwu(LiwuStat):
	def __init__(self, room_ctrl):
		self.room_ctrl = room_ctrl

		LiwuStat.__init__(self, room_ctrl)

		self.dbg_flag_add("LOGLIWU",	0)

		self.liwu_record_list = []

	def liwu_log(self, msg):
		uid   = msg['uid']
		nn    = msg['nn']
		cid   = msg['cid']
		level = msg['level']
		rid   = msg['rid']
		txt   = msg['txt']
		ic    = msg['ic']

		self.liwu_total += 1

		if self.dbg_flag_vaild("LOGLIWU"):
			tstr = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())

			sql = u'INSERT INTO liwu_log  (time, uid, nn, cid, level, rid, txt, ic) \
				VALUES("%s", "%s","%s","%s",%s,"%s","%s","%s");' %(tstr, uid, nn, cid, level, rid, txt, ic)

			self.db_submit(sql)

	def liwu_start(self):
		self.liwu_stat_start()

	def liwu_stop(self):
		self.liwu_stat_stop()

	# 监控弹幕
	def help_liwu_monitor(self):
		print    "   liwu_monitor [start|stop]"
		print    u"			 ----	发送弹幕"

	def do_liwu_monitor(self, line):
		argv = line.split()
		argc = len(argv)

		if argc > 1:
			self.help_liwu_monitor()
			return

		if argc == 0:
			print "liwu_monitor_state: ", self.liwu_monitor_state
		else:
			if argv[0] == "start":
				self.liwu_monitor_start()
			elif argv[0] == "stop":
				self.liwu_monitor_stop()
			else:
				self.help_liwu_monitor()
				return

#End of Liwu

if __name__ == '__main__':
	liwu = Liwu("LIWU")
	liwu.cmdloop()
#End of file

