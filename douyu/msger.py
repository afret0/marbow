# -*- coding: utf-8 -*-

import thread
import time
import logging
import uuid
import hashlib
import requests
import re
import sys
import json

from urllib import unquote

sys.path.append("..")

from hylib.cookie import *
from hylib.hyclass import *

from client import *

RAW_BUFF_SIZE = 4096
keeplive_INTERVAL_SECONDS = 30

COOKIE_FILE = 'marbow.cookie'
ACF_VER = '20150929'
ACF_AVER = '2016081801'

SAMPLE_PWD = '1234567890123456'
SUPPERGROUPID = -9999


class Msger(HYClass):
    def __init__(self, modid):

        self.client = None

        self.rid = None
        self.uid = None
        self.gid = SUPPERGROUPID

        self.msg_hanlder = {}

        HYClass.__init__(self, modid)

        self.dbg_flag_add("MSGR", 1)

    def msg_regiseter(self, msg_name, func):
        self.cnt_inc("msg_reged")   #此参数传递后方便统计总消息记录
        self.msg_hanlder[msg_name] = func #成功则置1
        self.dbg_verb("MSGR", 'Message of type "%s" register success' % msg_name)

    def gid_set(self, gid):
        self.dbg_noti("MSGR", 'Group id change %s -> %s' % (self.gid, gid))
        self.gid = gid

    def uid_get(self):
        return self.uid

    def get_longin_param_by_cookie(self, rid):
        # ccookies = get_chrome_cookies(DOUYU_DOMAIN)
        cookies = self.json_file_load(COOKIE_FILE)

        rt = str(int(time.time()))
        strs = rt + '7oE9nPEG9xXV69phU31FYCLUagKeYtsF' + cookies['acf_devid']
        vk = hashlib.md5(strs).hexdigest()

        param = {
            'type': 'loginreq',
            'username': cookies['acf_uid'],
            'password': cookies['acf_auth'],
            'ct': cookies['acf_ct'],
            'roomid': rid,
            'devid': cookies['acf_devid'],
            'rt': rt,
            'vk': vk,
            'ver': ACF_VER,
            'aver': ACF_AVER,
            'ltkid': cookies['acf_ltkid'],
            'biz': cookies['acf_biz'],
            'stk': cookies['acf_stk'],
        }

        self.dbg_verb("MSGR", param)
        return param

    def get_simple_longin_param(self, rid):
        param = {
            'type': 'loginreq',
            'username': self.uid,
            'password': SAMPLE_PWD,
            'roomid': rid,

        }

        self.dbg_verb("MSGR", param)
        return param

    def login(self, rid, uid):
        param = None
        mode = None

        if uid:
            self.uid = uid
            param = self.get_simple_longin_param(rid)
            mode = "sample"
        else:
            param = self.get_longin_param_by_cookie(rid)
            self.uid = param['username']
            mode = "cookie"

        self.client.send(param)

        self.rid = rid

        self.dbg_verb("MSGR", "Login param %s" % (param))

        self.dbg_noti("MSGR", "User %s login by %s success" % (self.uid, mode))

    def logout(self):
        self.rid = 0
        self.dbg_noti("MSGR", "User %s logout success" % (self.uid))

    def joingroup(self):
        self.client.send({'type': 'joingroup', 'rid': self.rid, 'gid': self.gid})
        self.dbg_noti("MSGR", "join to group %s " % self.gid)

    def loginres_hdlr(self, msg):
        self.joingroup()
        self.cnt_inc("loginres_hdlr")

    def keeplive_hdlr(self, msg):
        self.cnt_inc("keeplive_hdlr")

    def recv(self, client):
        # Handle messages
        for msg in client.receive():

            if not msg:
                continue

            self.cnt_inc("rx_msg")


            msg_type = msg.attr('type')

            # self.dbg_debug("MSGR", "msg_type: %s" % (msg_type))

            try:
                body_json_str = json.dumps(msg.body)
            except UnicodeDecodeError as e:
                self.cnt_inc("rx_decode_fail_msg")
                self.dbg_err("MSGR", 'Message decode fail!')
                continue

            self.dbg_verb("MSGR", body_json_str)
            self.cnt_inc(msg_type)

            try:
                handler = self.msg_hanlder[msg_type]
            except:
                self.cnt_inc("rx_unreg_msg")
                self.dbg_noti("MSGR", 'No handler of type "%s" ' % msg_type)
                continue

            self.cnt_inc("rx_reged_msg")
            handler(msg)


    # End of recv

    def sendmsg(self, msg):

        self.cnt_inc("tx_msg")

        send_par = {
            'type': 'chatmessage',
            'receiver': 0,
            'content': msg
        }

        self.client.send(send_par)
        self.dbg_debug("MSGR", msg)

    # End of send

    def keeplive(self, client, delay):
        while True:
            current_ts = int(time.time())
            data={'type': 'keeplive','tick': current_ts}

            client.send(data)

            time.sleep(delay)

    # End of keeplive

    def start(self, host, port, rid, uid):

        self.msg_regiseter('loginres', self.loginres_hdlr)
        self.msg_regiseter('keeplive', self.keeplive_hdlr)

        self.client = Client(host, port)

        self.dbg_noti("MSGR", "Connet to server %s:%d " % (host, port))

        self.login(rid, uid)

        # Start a thread to send keeplive messages separately
        thread.start_new_thread(self.keeplive, (self.client, keeplive_INTERVAL_SECONDS))

        # Start a thread to send keeplive messages separately
        thread.start_new_thread(self.recv, (self.client,))

    # End of start

    def stop(self):
        self.logout()
        # End of stop


# End of Msger

if __name__ == '__main__':
    Msger = Msger("MSGER")
    Msger.cmdloop()
