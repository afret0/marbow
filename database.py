#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import MySQLdb
import random

from hylib.hyclass import *

QA_TABLE = "marbow_qa"
DB_HOST = "192.168.33.26"

class Database(HYClass):
	def __init__(self, modid):
		HYClass.__init__(self, modid)
		self.dbg_flag_add("DB",	1)

	def db_submit(self, sql):
		self.dbg_verb("DB", sql)
		try:
			db = MySQLdb.connect(user='marbow', db='marbow', passwd='mb1q2w3e', host=DB_HOST, charset="utf8", port=3306)
			cursor = db.cursor()
			cursor.execute(sql)
			db.commit()
			db.close()
		except:
			self.cnt_inc("db_error")

	def db_select(self, sql):
		# type: (object) -> object
		self.dbg_verb("DB", sql)
		try:
			db = MySQLdb.connect(user='marbow', db='marbow', passwd='mb1q2w3e', host=DB_HOST, charset="utf8", port=3306)
			cursor = db.cursor()
			cursor.execute(sql)
			results = cursor.fetchall()
			db.close()
			return results
		except:
			self.cnt_inc("db_error")
			return None

	def db_answer_lookup_all(self, question):
		sql = 'SELECT a FROM %s where q="%s";' % (QA_TABLE, question)
		results = self.db_select(sql)

		if results:
			answers=[]
			for i in range(0, len(results)):
				answers.append(results[i][0])
			return answers
		else:
			return None

	def db_answer_lookup(self, question):
		answers = self.db_answer_lookup_all(question)

		if answers == None:
			return None

		num = len(answers)
		r = random.randint(0, (num - 1))

		return answers[r]

	def db_answer_exist(self, question, answer):
		answers = self.db_answer_lookup_all(question)

		if answers == None:
			return False

		for a in answers:
			if a == answer:
				return True

		return False

	def db_answer_add(self, question, answer):
		sql = 'INSERT INTO %s (q,a) VALUES("%s","%s");' % (QA_TABLE, question, answer)
		self.db_submit(sql)
		self.cnt_inc("local_answer_add")

	# 从数据库中存取会话
	def	help_db(self):
		print	"	 db QUESTION [ANSWER]"
		print	u"			 ---- 从数据库中存取答案 "
	
	def	do_db(self,	line):
		argv = line.split()
		argc = len(argv)
	
		if argc	== 1:
			question = argv[0]
			answer = self.db_answer_lookup(question)

			if answer:
				print answer
			else:
				print u"找不到答案 "

		elif argc == 2 and argv[1] == "all":
			question = argv[0]
			answers = self.db_answer_lookup_all(question)

			if answers == None:
				print u"找不到答案 "
				return
				
			num = len(answers)
			print u"找到%d个答案:" %(num)
			for i in range(0, num):
				answer =  answers[i]
				print u"  %.2d: %s" %(i,answer)
	
		elif argc == 2:
			question = argv[0]
			answer = argv[1]
			self.db_answer_add(question, answer)
        
		else:
			self.help_db()
#End of Database

if __name__ == '__main__':
	db = Database("DB")
	db.cmdloop()
#End of file
