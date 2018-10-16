#-*- coding: utf-8 -*-
import sys
reload(sys)

import json

from msger import *
from char import *

from zblib.zbroom import *




class DouyuRoom(DouyuUtils,Char,ZBRoom):
    def __init__(self, rid):
        self.dbg_flag_add("DYROOM", 1)

        Char.__init__(self, "DYROOM")
        ZBRoom.__init__(self, "DYROOM")
        DouyuUtils.__init__(self, "DYROOM")

        #self.gift_tab = globalValue.value
        self.info["platform"] = "douyu"
        self.info["roomid"] = rid
        self.rid=rid
        self.ginfo=self.get_gift_list(rid)

        self.data_msger.msg_regiseter('chatmsg', self.charmsg_hdlr) # 弹幕
        self.data_msger.msg_regiseter('chatres', self.chatres_hdlr) # 弹幕回应
        self.data_msger.msg_regiseter('dgb', self.dbg_hdlr) # 礼物
        self.data_msger.msg_regiseter('onlinegift', self.onlinegift_hdlr) # 领取礼物
        self.data_msger.msg_regiseter('bc_buy_deserve', self.bc_buy_deserve_hdlr) # 超级酬勤
        self.data_msger.msg_regiseter('ggbb', self.def_hdlr)
        self.data_msger.msg_regiseter('uenter', self.def_uenter_hdlr) #用户进入直播间
        self.data_msger.msg_regiseter('ranklist', self.def_hdlr)
        self.data_msger.msg_regiseter('srres', self.def_hdlr) #用户分享直播间
        self.data_msger.msg_regiseter('spbc', self.def_hdlr)
        self.data_msger.msg_regiseter('gift_title', self.def_hdlr)
        self.data_msger.msg_regiseter('rankup', self.def_hdlr)
        self.data_msger.msg_regiseter('ul_ranklist', self.def_hdlr)
        self.data_msger.msg_regiseter('ruclp', self.def_hdlr)
        self.data_msger.msg_regiseter('upgrade', self.def_hdlr)
        self.data_msger.msg_regiseter('newblackres', self.def_hdlr) #用户禁言
        self.data_msger.msg_regiseter('rss', self.def_hdlr)
        self.data_msger.msg_regiseter('donateres', self.def_hdlr)
        self.data_msger.msg_regiseter('setadminres', self.def_hdlr)


        self.data_msger.msg_regiseter('rsm', self.def_hdlr) #新注册messge 20161229
        self.data_msger.msg_regiseter('error', self.def_hdlr)
        self.data_msger.msg_regiseter('scl', self.def_hdlr)
        self.data_msger.msg_regiseter('suq', self.def_hdlr)
        self.data_msger.msg_regiseter('initcl', self.def_hdlr)
        self.data_msger.msg_regiseter('memberinfores', self.def_hdlr)
        self.data_msger.msg_regiseter('rri', self.def_hdlr)
        self.data_msger.msg_regiseter('rlcn', self.def_hdlr)

    def def_uenter_hdlr(self, msg):
        self.cnt_inc("self.def_uenter_hdlr")
        self.hdlr_call("uenter", msg)


    def def_hdlr(self,msg):
        self.cnt_inc("self.def_hdlr")


    def charmsg_hdlr(self, msg):

        self.cnt_inc("self.charmsg_hdlr")
        data = {'platfrom':"douyu",
                'type':"danmu", #添加消息类型
                'nn':msg.body['nn'],
                'uid':msg.body['uid'],
                'rid':msg.body['rid'],
                'level':msg.body['level'],
                'time': time.strftime('%Y-%m-%d %X', time.localtime(time.time())), #添加消息发生时间
                'txt':msg.body['txt']}
        self.hdlr_call("char", data)
        #print "New  message::",json.dumps(data,encoding='utf-8',ensure_ascii=False)
        #with open("chat_"+time.strftime('%Y-%m-%d', time.localtime(time.time()))+msg.body['rid'] + '.txt', 'a+') as f:  # 20161228修改
        #   f.write(json.dumps(data,encoding='utf-8',ensure_ascii=False)+'\n')

    def chatres_hdlr(self, msg):
        self.cnt_inc("self.chatres_hdlr")

    def dbg_hdlr(self, msg):
        self.cnt_inc("self.def_hdlr")
        '''
        ID    ： ", gtype['id']
        name  ： ", gtype['name']
        type  ： ", gtype['type']
        pc    ： ", gtype['pc']
        gx    ： ", gtype['gx']
        desc  ： ", gtype['desc']
        intro ： ", gtype['intro']
        mimg  ： ", gtype['mimg']
        himg  ： ", gtype['himg']
        '''
        gname=None
        pc=None
        for gtype in self.ginfo:
            if int(msg.body['gfid'])==int(gtype['id']):
                gname=gtype['name']
                pc=gtype['pc']

        data = {
            'uid': msg.body['uid'],
            'type':'liwu',
            'nickname': msg.body['nn'],
            'level': msg.body['level'],
            'gid': msg.body['gfid'],
            'rid': msg.body['rid'],
            'time': time.strftime('%Y-%m-%d %X', time.localtime(time.time())),  # 添加消息发生时间
            'numb': 1,
            'gname':gname,
            'pc':pc
            }

        self.hdlr_call("gift", data)
        ##with open("gift_"+time.strftime('%Y-%m-%d', time.localtime(time.time()))+msg.body['rid'] + '.txt', 'a+') as f:  # 20161228修改
        ##   f.write(json.dumps(data,encoding='utf-8',ensure_ascii=False)+'\n')

    def onlinegift_hdlr(self, msg):
        self.cnt_inc("self.onlinegift_hdlr")


    def bc_buy_deserve_hdlr(self, msg):
        self.cnt_inc("self.bc_buy_deserve_hdlr")


    def gift_list_update(self):

        ret = self.get_gift_list(self.rid)

        if ret == None:
            print "无法获取直播间%s的礼物列表" % (rid)
            return False

        for gtype in ret:
            gift = self.gift_get(gtype['id'])
            if gift == None:
                gift = {"gid" : gtype['id'], "name" : gtype['name'], "value" : gtype['gx'], "img" : gtype['mimg']}
                self.gift_list.append(gift)

    def update(self):
        ret = self.get_room_info(self.info["roomid"])

        self.info["zhubo"]  = ret['owner_name']
        self.info["title"]  = ret['room_name']
        self.info["ontime"] = ret['start_time']
        self.info["block"]  = ret['cate_name']
        self.info["fans"]   = ret['fans_num']
        self.info["audience"] = ret['online']



        if ret['start_time'] == 1:
            self.info["state"] = "online"
            self.online()
        else:
            self.info["state"] = "offline"
            self.offline()

        self.gift_list_update()


    def login(self):

        return self.char_enter(self.rid)

    def logout(self):
        return self.char_exit()

    # 发生弹幕 data {"type": STR,"txt": TXT}
    def char_send(self, data):
        self.msgsend(data['txt'])

    # 赠送礼物 data {"name": STR， "number": INIT 服务·4}
    def gift_send(self, data):
        cdata = {
            'userid': self.info['userid'],
            'nickname': self.info['nickname'],
            'level': 0,
            'gift': data['type'],
            'numb': data['numb']
        }

        self.hdlr_call("gift", cdata)

        return True

    # 发生通告 data {"name": STR， "number": INIT 服务·4}
    def noti_send(self, data):
        return False

    # 关注
    def follow(self):
        self.msgsend("#关注")
        return True

    # 取关
    def unfollow(self):
        self.msgsend("#取关")
        return True

# End of Room

if __name__ == '__main__':
    room = DouyuRoom("106119")
    room.cmdloop()