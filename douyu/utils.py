# -*- coding: utf-8 -*-

import sys

sys.path.append("..")

import json
import requests

from hylib.hyclass import *

DOUYU_GIFT_INFO = [
    {"gid": 511, "name": "圣诞火箭", "value": 5000},
    {"gid": 510, "name": "圣诞飞机", "value": 1000},
    {"gid": 509, "name": "姜饼屋", "value": 60},
    {"gid": 508, "name": "小雪人", "value": 2},
    {"gid": 507, "name": "圣诞赞一个", "value": 1},
    {"gid": 506, "name": "冰淇淋球", "value": 1},
    {"gid": "cq", "name": "酬勤", "value": 0},

]


class DouyuUtils(HYClass):
    def __init__(self, modid):
        HYClass.__init__(self, modid)
        self.dbg_flag_add("DYUTIL", 0)

    def get_gift_info(self, gid):
        for gift in DOUYU_GIFT_INFO:
            if gid == gift["gid"]:
                return gift

        return None

    def get_room_info(self, room_id):
        header = {
            'Host': "www.douyu.com",
            'Referer': "http://www.douyu.com/",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        }

        ret = []

        search_url = 'http://open.douyucdn.cn/api/RoomApi/room/%s' % (room_id)

        try:
            r = requests.get(search_url)
        except:
            return None

        response = r.text
        room = json.loads(response)

        if (room['error'] == 0):
            data = room['data']

            if data['room_status'] == '1':
                reachable = 1
            else:
                reachable = 0
        else:
            return None

        return data



    # 获取房间信息
    def help_roominfo(self):
        print    "   roominfo ROOMID"
        print    "			 ----	获取直播间信息"

    def do_roominfo(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 1:
            self.help_roominfo()
            return False

        rid = argv[0]

        ret = self.get_room_info(rid)

        if ret == None:
            print "无法获取直播间%s的信息" % (rid)
            return False

        print "房间  ： ", ret['room_id']
        print "截图  ： ", ret['room_thumb']
        print "板号  ： ", ret['cate_id']
        print "板块  ： ", ret['cate_name']
        print "标题  ： ", ret['room_name']
        print "主播  ： ", ret['owner_name']
        print "头像  ： ", ret['avatar']
        print "人气  ： ", ret['online']
        print "体重  ： ", ret['owner_weight']
        print "关注  ： ", ret['fans_num']
        print "开播  ： ", ret['start_time']

    def get_gift_list(self, room_id):
        header = {
            'Host': "www.douyu.com",
            'Referer': "http://www.douyu.com/",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        }

        ret = []

        search_url = 'http://open.douyucdn.cn/api/RoomApi/room/%s' % (room_id)

        try:
            #r = requests.get(search_url, headers=header)
            r = requests.get(search_url)
        except:
            return None

        response = r.text
        room = json.loads(response)


        if (room['error'] == 0):
            data = room['data']

            if data['room_status'] == '1':
                reachable = 1
            else:
                reachable = 0
        else:
            return None

        return data['gift']

    # 获取房间信息
    def help_get_gift_list(self):
        print    "   room_gift_lis ROOMID"
        print    "			 ----	获取直播间礼物列表"

    def do_get_gift_list(self, line):

        argv = line.split()
        argc = len(argv)

        if argc != 1:
            self.help_get_gift_list()
            return False

        rid = argv[0]

        ret = self.get_gift_list(rid)

        if ret == None:
            print "无法获取直播间%s的礼物列表" % (rid)
            return False

        for gtype in ret:
            '''
           "id":"196" ,
            "name":"\u706b\u7bad" ,
            "type":"2" ,
            "pc":500 ,
            "gx":5000 ,
            "desc":"\u8d60\u9001\u7f51\u7ad9\u5e7f\u64ad\u5e76\u6d3e\u9001\u51fa\u795e\u79d8\u5b9d\u7bb1" ,
            "intro":"\u6211\u4eec\u7684\u5f81\u9014\u662f\u661f\u8fb0\u5927\u6d77" ,
            "mimg":"http:\/\/staticlive.douyucdn.cn\/upload\/dygift\/1606\/26f802520cf0e4d8a645259bbc1aadf3.png" ,
            "himg":"http:\/\/staticlive.douyucdn.cn\/upload\/dygift\/1606\/39b578b3cb8645b54f9a1001c392a237.gif"
            '''
            print "  ================================================================================================="
            print "    ID    ： ", gtype['id']
            print "    name  ： ", gtype['name']
            print "    type  ： ", gtype['type']
            print "    pc    ： ", gtype['pc']
            print "    gx    ： ", gtype['gx']
            print "    desc  ： ", gtype['desc']
            print "    intro ： ", gtype['intro']
            print "    mimg  ： ", gtype['mimg']
            print "    himg  ： ", gtype['himg']




# End of Utils

if __name__ == '__main__':
    utils = DouyuUtils("utils")
    utils.cmdloop()
