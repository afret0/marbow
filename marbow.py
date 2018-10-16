#-*- coding: utf-8 -*-

import sys
reload(sys)
#sys.setdefaultencoding('utf-8')

import time
import thread

from zhibojian import *

import chardet

from tuling import *
from danmu import *
from danmu_stat import  *

DEF_MON_PERIOD = 3

class Marbow(HYClass):

	def __init__(self):
		self.zhibojian_list = {}
		self.state = False
		self.period = DEF_MON_PERIOD

		HYClass.__init__(self, "MB")

		self.dbg_flag_add("INIT", 1)

	def get_zhibojian_by_rid(self, rid):
		try:
			return self.zhibojian_list[rid]
		except:
			return None

	def zhibojian_add(self, rid):

		zhibojian = self.get_zhibojian_by_rid(rid)

		if zhibojian != None:
			return False


		zhibojian = Zhibojian('douyu',rid)

		self.zhibojian_list[rid] = zhibojian

		return True

	def zhibojian_del(self, rid):
		del self.zhibojian_list['rid']

	def mon_start(self, rid):

		for zhibojian in self.zhibojian_list.values():
			zhibojian.start()

	def mon_stop(self):
		self.state = 1



	# 获取房间信息
	def help_add(self):
		print    "   add RID"
		print    "			 ----	添加监控直播间"

	def do_add(self, line):
		argv = line.split()
		argc = len(argv)

		if argc != 1:
			self.help_add()

		rid = argv[0]

		self.zhibojian_add(rid)

	# 获取房间信息
	def help_del(self):
		print    "   del RID"
		print    "			 ----	移除监控直播间"

	def do_del(self, line):
		argv = line.split()
		argc = len(argv)

		if argc != 1:
			self.help_del()

		rid = argv[0]

		self.zhibojian_del(rid)

	# 获取房间信息
	def help_status(self):
		print    "   status"
		print    "			 ----	现实监控状态"

	def do_status(self, line):
		argv = line.split()
		argc = len(argv)

		if argc != 0:
			self.help_status()

		for zhibojian in self.zhibojian_list.values():
			print "%6s : %s" %(zhibojian.rid, self.state)

		# 启动监控

	def help_start(self):
		print    "   start [RID]"
		print    "			 ----	启动直播间"

	def zhibojian_start(self, zhibojian):
		rt = zhibojian.start()

		if rt == True:
			print "直播间%s ..... 启动成功！" % (zhibojian.rid)
		else:
			print "直播间%s ..... 启动失败！" % (zhibojian.rid)

	def do_start(self, line):
		argv = line.split()
		argc = len(argv)

		if argc > 1:
			self.help_start()

		if argc == 0:
			for zhibojian in self.zhibojian_list.values():
				self.zhibojian_start(zhibojian)
		else:
			rid = argv[0]
			zhibojian = self.get_zhibojian_by_rid(rid)

			if zhibojian == None:
				print "未找到直播间: %s!" %(rid)
				return

			self.zhibojian_start(zihbojian)

		# 停止监控

	def help_stop(self):
		print    "   stop"
		print    "			 ----	停止监控状态"

	def do_stop(self, line):
		argv = line.split()
		argc = len(argv)

		if argc != 0:
			self.help_stop()

		if argc > 1:
			self.help_start()

		if argc == 0:
			for zhibojian in self.zhibojian_list.values():
				zihbojian.stop()
		else:
			rid = argv[0]
			zhibojian = self.get_zhibojian_by_rid(rid)

			if zhibojian == None:
				print "未找到直播间: %s!" %(rid)
				return

				zihbojian.stop()

	def help_zhibojian(self):
		print    "   zhibojian [RID]"
		print    "			 ---- 进入直播间命令行模式"

	def do_zhibojian(self, line):
		argv = line.split()
		argc = len(argv)

		if argc > 1:
			self.help_zhibojian()
			return

		rid = argv[0]

		zhibojian = self.get_zhibojian_by_rid(rid)

		if zhibojian == None:
			print "未找到直播间"
			return

		#thread.start_new_thread(zhibojian.cmdloop(), (zhibojian,))
		zhibojian.prompt = 'ZBJ(%s): ' %(zhibojian.rid)
		zhibojian.cmdloop()

#End of Marbow

if __name__ == '__main__':
	marbow = Marbow()
	marbow.prompt = 'MARBOW: '
	marbow.cmdloop()


		
#End of file



