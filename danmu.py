#-*- coding: utf-8 -*-

import sys
reload(sys);
sys.setdefaultencoding('utf-8');

import time
import MySQLdb
import thread
from douyu.char import *
from danmu_talk import *
from danmu_stat import  *
from danmu_word import  *

class Danmu(DanmuStat, DanmuTalk, DanmuWord):
	def __init__(self, room_ctrl):
		self.room_ctrl = room_ctrl

		DanmuStat.__init__(self, room_ctrl)
		DanmuTalk.__init__(self, room_ctrl)
		DanmuWord.__init__(self, room_ctrl)

		self.dbg_flag_add("LOGDANMU",	0)

		self.danmu_record_list = []

	def danmu_start(self):
		self.talk_start()
		self.danmu_stat_start()
		self.word_start()

	def danmu_stop(self):
		self.talk_stop()
		self.danmu_stat_stop()
		self.word_stop()

	# 发送弹幕
	def	help_danmu(self):
		print	"   danmu WORDS"
		print	u"			 ----	发送弹幕"

	def	do_danmu(self, line):
		argv = line.split()
		argc = len(argv)

		if argc	!= 1:
			self.help_danmu()

		msg = argv[0]

		self.danmu_send(msg)

	# 监控弹幕
	def help_danmu_monitor(self):
		print    "   danmu_monitor [start|stop]"
		print    u"			 ----	发送弹幕"

	def do_danmu_monitor(self, line):
		argv = line.split()
		argc = len(argv)

		if argc > 1:
			self.help_danmu()
			return

		if argc == 0:
			print "danmu_monitor_state: ", self.danmu_monitor_state
		else:
			if argv[0] == "start":
				self.danmu_monitor_start()
			elif argv[0] == "stop":
				self.danmu_monitor_stop()
			else:
				self.help_danmu()
				return

#End of Danmu

if __name__ == '__main__':
	danmu = Danmu("DANMU")
	danmu.cmdloop()
#End of file

