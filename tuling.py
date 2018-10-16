#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import json
import urllib2, urllib
import requests

from hylib.hyclass import	*


TALK_URL	=	"http://www.tuling123.com/openapi/api"
IFAQ_URL	=	"http://www.tuling123.com/v1/setting/importfaq"
SFAQ_URL	=	"http://www.tuling123.com/v1/setting/selectfaq"
UFAQ_URL	=	"http://www.tuling123.com/v1/setting/updatefaq"
DFAQ_URL	=	"http://www.tuling123.com/v1/setting/deletefaq"
RENN_URL	=	"http://www.tuling123.com/v1/setting/setnickname"

MARBOW_KEY = u'1f0d017fd2f84a4683a9a7a1ad455910'

tuling_code_list = {
    '101': u"请求内容为空",
    '201': u"请求超时",
    '301': u"异常信息(json格式错误，500错误等)",
    '401': u"账号不合法",
    '403': u"账号上传权限已经用尽",
    '404': u"账号没有知识库接口使用权限",
    '405': u"账号开启安全模式，token校验失败",
    '501': u"json请求的内容有误",
    '40001': u"key 长度错误(32位)",
    '40002': u"在的，请说",
    '40003': u"当天请求的次数超限制",
    '40004': u"api服务器错误"
}

class Tuling(HYClass):
	
	def	__init__(self, modid):
		self.key = MARBOW_KEY
		
		HYClass.__init__(self, modid)

		self.dbg_flag_add("TULI",	1)
		self.dbg_flag_add("FAQ",	1)
		self.dbg_noti("TULI",	"Tuling	on duty")
		
	def	dump(self, str):
		str	=	str.decode('utf-8').encode('gbk')
		print	str

	#   交谈, HTTP GET方式
	def	tuling_answer_lookup(self, string):
		#uri	=	TALK_URL + "?key=" + self.key	+	"&info=" + string
		uri = u"%s?key=%s&info=%s" %(TALK_URL, self.key, string)
		res	=	urllib2.urlopen(uri).read()
		res_dict = json.loads(res)
		code = "%s" %(res_dict["code"])

		try:
			msg	=	tuling_code_list[code]
			self.cnt_inc("talk_err_%s" %(code))
		except:
			msg	=	self.productMsg(res_dict,	code)
		
		return msg

	def	help_tuling(self):
		print	"	 tuling QUESTION"
		print	u"			 ----	与图灵对话"

	def	do_tuling(self,	line):
		argv = line.split()
		argc = len(argv)

		if argc	!= 1:
			self.help_tuling()

		keyword	= argv[0]
		answer	= self.tuling_answer_lookup(keyword)

		print answer


	#	通用知识库操作函数, HTTP POST方式
	def	faqop(self,	url, sjson):
		self.dbg_verb("FAQ", url)
		self.dbg_verb("FAQ", sjson)
			
		try: 
			sdata = json.JSONEncoder().encode(sjson)
			response = urllib2.urlopen(url, sdata)
			res = response.read()
		except :
			self.dbg_debug("FAQ", "Post error!")
		
		rjson =	json.loads(res)

		code = rjson["code"]
		data = rjson["data"]

		self.dbg_verb("FAQ", "CODE = %s"	%(code))
		self.dbg_verb("FAQ", "DATA = %s"	%(data))
		
		if code	== 0:
			self.dbg_debug("FAQ", u"%s,	请求成功." % (url))
			return rjson["data"]
		
		#后面的代码在返回错误的时候才回被执行
		ckey = "%d" %code
		
		if tuling_code_list[ckey]:
			self.dbg_err("FAQ", tuling_code_list[ckey])
			self.cnt_inc("faq_err_%d" %(ckey))
		else:
			self.dbg_err("FAQ",	"未知错误: %d" %(code))
			self.cnt_inc("faq_err_unkonw")

		return None
		
			
	#	搜索知识库
	def	sfaq(self, keyword):



		pageNumber = 1
		pageSize = 100
	

		sjson = {
      "apikey": self.key,
      "data":{
        "pages":{
            "pageNumber": 1,
            "pageSize": pageSize,
            "searchBy": keyword
        }
      }
    }
    
		rjson =	self.faqop(SFAQ_URL, sjson)

		if rjson == None:
			return alist

		totalCount = rjson['totalCount']
		
		if totalCount == 0:
			return alist

		rlist =	rjson['knowledgeList']

			
		return rlist


	def	help_sfaq(self):
		print	"	 sfaq	KEYWORD"
		print	u"			 ----	查找知识库"

	def	do_sfaq(self,	line):
		argv = line.split()
		argc = len(argv)

		if argc	!= 1:
			self.help_sfaq()

		keyword	= argv[0]
		faqlist	= self.sfaq(keyword)

		if faqlist:
			for	item in	faqlist:
				id = item['id']
				question = item['question']
				answer = item['answer']
				time = item['time']

				print	"%5s:	%s %s	%s"	%(id,	question,	answer,	time)

		else:
			print	u"未找到对应答案！"

	def	ifaq(self, faqlist):
		sjson	=	{
			u"apikey": self.key,
			u"data": faqlist
		}
		
		rjson	=	self.faqop(IFAQ_URL, sjson)
		
		if rjson:
			return True
		else:
			return False

	def	help_ifaq(self):
		print	"	 ifaq	QUESTION ANSWER"
		print	u"			 ----	添加知识库"

	def	do_ifaq(self,	line):
		argv = line.split()
		argc = len(argv)

		if argc	!= 2:
			self.help_ifaq()

		question = argv[0]
		answer	 = argv[1]

		faqlist	= [{"question": question, "answer": answer}]

		if self.ifaq(faqlist):
			print	u"知识库添加成功"
		else:
			print	u"知识库添加失败！"

	#	修改知识库
	def	ufaq(self, faqlist):
		sjson = {
			"apikey": self.key,
			"data": faqlist
		}

		if self.faqop(UFAQ_URL,	sjson):
			return True
		else:
			return False

	def	help_ufaq(self):
		print	"	 ufaq	ID ANSWER"
		print	u"			 ----	修改知识库"

	def	do_ufaq(self,	line):
		argv = line.split()
		argc = len(argv)

		if argc	!= 2:
			self.help_ufaq()

		id = argv[0]
		answer	 = argv[1]

		faqlist	= [{"id": id, "answer": answer}]

		if self.ufaq(faqlist):
			print	u"修改库添加成功"
		else:
			print	u"修改库添加失败！"

	#	删除知识库表项
	def	dfaq(self, ids):
		sjson	=	{
			"apikey":	self.key,
			"data":	{
				"clear":{"isclear":	False},
				"ids": ids
			}
		}

		if self.faqop(UFAQ_URL,	sjson):
			return ture
		else:
			return False
	
	def	help_dfaq(self):
		print	"	 dfaq	IDS"
		print	u"			 ----	删除知识库"

	def	do_dfaq(self,	line):
		argv = line.split()
		argc = len(argv)

		if argc	!= 2:
			self.help_dfaq()

		ids = argv[0]

		faqlist	= [{"id": [ids]}]

		if self.dfaq(faqlist):
			print	u"修改库添加成功"
		else:
			print	u"修改库添加失败！"

	#	清空知识库
	def	cfaq(self, ids):
		sjson	=	{
			"apikey":	self.key,
			"data":	{
				"clear":{"isclear":	true},
				"ids": ids
			}
		}

		if self.faqop(UFAQ_URL,	sjson):
			return ture
		else:
			return False

				
	#	修改机器人名称
	def	renn(self, name):
		sjson = {
			"apikey":	self.key,
			"data": name
		}


	#	这里处理错误的相应码
	def	talk_code_check(self,	code):
		if code	== 40001:
			self.dump(u"key 长度错误(32位)")
			return False
		elif code	== 40002:
			self.dump(u"请求的内容是空")
			return False
		elif code	== 40003:
			self.dump(u"当天请求的次数超限制")
			return False
		elif code	== (40004 or 40005 or 40006 or 40007):
			error_msg	=	u"api服务器错误	#" + code
			self.dump(error_msg)
			return False
		else:
			return code

	#	这里生成输出的信息	里面的代码可以去文档里看
	def	productMsg(self, res_dict, code):
		
		output = res_dict["text"]	+	"\r\n"
		self.dbg_debug("TULI", "code:%s, output=%s" %(code, output))
		text = ""
		if code	== '200000':
			text = "请打开	"	+	 res_dict["url"]
		elif code	== '302000':
			ablist = res_dict['list']
			for	index	in range(len(ablist)):
				alist	=	ablist[index]
				tmp	=	alist["article"] + "--"	+	alist["source"]	+	"——详情:"	+	alist["detailurl"] + "\r\n"
				text +=	tmp
		elif code	== '304000':
			ablist = res_dict['list']
			for	index	in range(len(ablist)):
				alist	=	ablist[index]
				tmp	=	alist["name"]	+	"--" + alist["count"]	+	"——详情" + alist["detailurl"]	+	"\r\n"
				text +=	tmp
		elif code	== '305000':
			ablist = res_dict['list']
			for	index	in range(len(ablist)):
				alist	=	ablist[index]
				tmp	=	alist["trainnum"]	+	"--" + alist["start"]	+	"("	+	alist["starttime"] + ")->" + alist["terminal"] + "(" + alist["endtime"]	+	")详情"	+	alist["detailurl"] + "\r\n"
				text +=	tmp
		elif code	== '306000':
			ablist = res_dict['list']
			for	index	in range(len(ablist)):
				alist	=	ablist[index]
				tmp	=	alist["flight"]	+	"--" + alist["route"]	+	"--起飞时间:"	+	alist["starttime"] + "--到达时间:" + alist["endtime"]	+	"--状态:"	+	alist["state"] + "--详情:" + alist["detailurl"]	+	"\r\n"
				text +=	tmp
		elif code	== '308000':
			ablist = res_dict['list']
			for	index	in range(len(ablist)):
				alist	=	ablist[index]
				tmp	=	alist["name"]	+	"--" + alist["info"] + "——详情:" + alist["detailurl"]	+	"\r\n"
				text +=	tmp
		elif code	== '309000':
			ablist = res_dict['list']
			for	index	in range(len(ablist))	:
				alist	=	ablist[index]
				tmp	=	alist["name"]	+	"-------"	+	alist["price"] + "--------"	+	alist["satisfaction"]
			text +=	tmp
		elif code	== '311000':
			ablist = res_dict['list']
			for	index	in range(len(ablist))	:
				alist	=	ablist[index]
				tmp	=	alist["name"]	+	"-------"	+	alist["price"] + "--详情：" + alist["detailurl"]
				text +=	tmp
		elif code	== '500000':
			text +=	"不知道你说的什么"
		
		return output	+	text

if __name__	== "__main__":
	tuling = Tuling("TULI")
	tuling.cmdloop()
