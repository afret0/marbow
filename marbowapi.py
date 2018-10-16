# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import time
import random
import json
import thread
import os
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify

from functools import wraps
from flask import make_response
from zhibojian import *

from marbow import *
import re

marbow = Marbow()
marbow.__init__()


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst

    return wrapper_fun


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello! This marbow API. Version V0.1"


# Global varibale

liwu = 0
guanzhu = 0
zhuyaoshuju_records = []
tpoint = {'pre': None}
user_id = {'uid': None}


def zhuyaoshuju_record_gen(rid, tstr):
    global liwu
    global guanzhu

    renqi = random.randint(10000, 30000)
    danmu = random.randint(10, 50)
    liwu += random.randint(0, 20)
    guanzhu += random.randint(0, 10)

    if tstr == None:
        tstr = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())

    data = {"time": tstr, "rid": rid, "renqi": renqi, "danmu": danmu, "liwu": liwu, "guanzhu": guanzhu}

    return data


# roomid
@app.route("/getid")
@allow_cross_domain
def getid():
    import MySQLdb
    id = int(request.args.get('loc_id', 0))
    data = {'loc_id': 0}
    try:
        conn = MySQLdb.connect('192.168.3.56', 'root', 'root', 'test')
        cur = conn.cursor()
        cur.execute('select * from roomid where id="%s"' % (id))
        if int(cur.fetchone()[0]):
            data['loc_id'] = 1
            conn.close()
    finally:
        return jsonify(data)


@app.route("/login", methods=['POST', 'GET', 'PUT'])  # 直播间登陆注册，开始直播间统计
@allow_cross_domain
def login():
    data = {'error': 1}
    room_id = request.args.get('loc_id', 0)
    if room_id not in marbow.zhibojian_list.keys():
        marbow.zhibojian_add(room_id)
        marbow.mon_start(room_id)
        data['error'] = 0
    else:
        data['error'] = 0
    return jsonify(data)


# interface 1
@app.route("/zaiyaoshuju", methods=['POST', 'GET', 'PUT'])
@allow_cross_domain
def zaiyaoshuju():
    rid = str(request.args.get('loc_id', 0))

    global marbow
    zhibojian = marbow.get_zhibojian_by_rid(rid)
    if zhibojian == None:
        sdata = {"error": 1, "rid": rid, "msg": "Zhibojian not exist!"}
        return jsonify(sdata)
    renqi = zhibojian.renqi_ctrl.renqi_total
    guanzhu = zhibojian.guanzhu_ctrl.guanzhu_total
    danmu = zhibojian.danmu_ctrl.danmu_total
    liwu = zhibojian.liwu_ctrl.liwu_total

    tstr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    sdata = {"error": 0, "time": tstr, "rid": rid, "renqi": renqi, "danmu": danmu, "liwu": round(liwu, 2),
             "guanzhu": guanzhu}

    return jsonify(sdata)


def zhuyaoshuju_record_get(stime, rnum):
    cnt = 0
    numb = len(zhuyaoshuju_records)
    records = []

    #    ts = time.strptime(stime, "%Y-%m-%d %H:%M:%S")

    if stime == "start":
        s = 0
    else:
        for s in range(0, numb):
            record = zhuyaoshuju_records[s]
            tr = time.strptime(record['time'], "%Y-%m-%d %H:%M:%S")
            if tr > ts:
                break

    for i in range(0, 0):
        records.append(zhuyaoshuju_records[i])
        cnt += 1
        if cnt >= rnum:
            break

    return records


# interface 2
@app.route("/lishishuju")
@allow_cross_domain
def lishishuju():
    rid = 0
    # rdata = {"rid":rid, “start_time”:“(start|YYYY-MM-DD hh:mm:ss”, “number”:“10”}
    rdata = request.get_data()

    try:
        rjson = json.loads(req)
        rid = rjson['rid']
        stime = rjson['start_time']
        rnum = rjson['num']

        print rjson
    except:
        rid = 0
        stime = "start"
        rnum = 0

    snum = 0

    records = zhuyaoshuju_record_get(stime, rnum)

    sdata = {
        "rid": rid, "number": snum,
        "record": [records]
    }

    return jsonify(sdata)


# interface 3
@app.route("/huoyueyonghu")
@allow_cross_domain
def huoyueyonghu():
    rid = str(request.args.get('loc_id', 0))

    global marbow
    zhibojian = marbow.get_zhibojian_by_rid(rid)
    if zhibojian == None:
        sdata = {"error": 1, "rid": rid, "msg": "Zhibojian not exist!"}
        return jsonify(sdata)

    '''result={uid:{'values':num,'rank':num,'nn':str,'level':num,'rid':num,'txt':{'2016-01-02 00:00:00','你好'}}}
    '''
    tmp = zhibojian.liwu_ctrl.result
    records = []
    for key, value in tmp.items():
        records.append({"uid": key, "nn": value['nn'], "level": value['level'], 'rank': value['rank']})
    sorted_records = sorted(records, key=lambda records: records['rank'])  # 0-9 依次表示送的礼物最多到最低的顺序
    sdata = {
        "rid": rid, "number": len(tmp),
        "shuiyou": sorted_records
    }
    return jsonify(sdata)


# interface 4
@app.route("/shuiyoudongtai")
@allow_cross_domain
def shuiyoudongtai():
    rid = str(request.args.get('loc_id', 0))

    global marbow
    zhibojian = marbow.get_zhibojian_by_rid(rid)
    sdata = {'msg': []}
    if zhibojian == None:
        sdata = {"error": 1, "rid": rid, "msg": "Zhibojian not exist!"}
        return jsonify(sdata)

    '''result={uid:{'values':num,'rank':num,'nn':str,'level':num,'rid':num}}
    '''
    stmp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    tmp = zhibojian.liwu_ctrl.result  # 后面需要将以前消息删除掉，暂时没有写
    mesg = zhibojian.liwu_ctrl.records
    for msg in mesg:
        if msg['time'] < tpoint['pre']:
            mesg.remove(msg)

    for key, value in tmp.items():
        if len(mesg):
            data = {"rid": rid, "uid": key, "nn": value['nn'], "numb": 10, "gifts": value['values'], "danmu": 30,
                    'level': value['level'],
                    "record": [var for var in mesg if var['uid'] == str(key)]
                    }
            sdata['msg'].append(data)
        else:
            data = {"rid": rid, "uid": key, "nn": value['nn'], "numb": 10, "gifts": value['values'],
                    "danmu": 30,
                    "record": []}
            sdata['msg'].append(data)
    tpoint['pre'] = stmp

    return jsonify(sdata)


# @app.route("/tuiguangxingxi")
# @allow_cross_domain
# interface 5
@app.route("/tuiguangxingxi")
@allow_cross_domain
def tuiguangxingxi():
    rid = 0
    # rdata = {"rid": rid, "uid": uid}
    rdata = request.get_data()

    try:
        rjson = json.loads(req)
        rid = rjson['rid']

        print rjson
    except:
        rid = 0

    sdata = {
        "rid": rid, "start_time": "2016-11-25 01:48:23", "number": 2,
        "record": [
            {"time": "2016-11-25 01:48:23", "rid": "122233", "nn": "less", "level": 12, "IP": "119.98.23.88",
             "status": "old"},
            {"time": "2016-11-25 01:48:35", "rid": "122235", "nn": "火锅", "level": 26, "IP": "119.98.23.89",
             "status": "new"}
        ]
    }

    return jsonify(sdata)


# interface 6
@app.route("/zuixinjilu")
@allow_cross_domain
def zuixinjilu():
    rid = 0
    # rddata = {"rid": rid}
    rdata = request.get_data()

    try:
        rjson = json.loads(req)
        rid = rjson['rid']

        print rjson
    except:
        rid = 0

    sdata = {
        "rid": rid, "modify_time": "2016-11-25 14:58:03", "number": 10,
        "record": [
            {"type": "danmu", "time": "2016-11-25 01:48:23", "uid": "122331", "nn": "less", "level": 13, "txt": "测试1"},
            {"type": "danmu", "time": "2016-11-25 01:51:35", "uid": "122331", "nn": "less", "level": 13, "txt": "测试2"},
            {"type": "danmu", "time": "2016-11-25 01:55:48", "uid": "122331", "nn": "less", "level": 13, "txt": "测试3"},
            {"type": "danmu", "time": "2016-11-25 01:56:48", "uid": "122331", "nn": "less", "level": 13, "txt": "测试4"},
            {"type": "danmu", "time": "2016-11-25 01:57:48", "uid": "122331", "nn": "less", "level": 13, "txt": "测试5"},
            {"type": "liwu", "time": "2016-11-25 01:42:23", "uid": "122331", "nn": "less", "level": 13, "gfid": "火箭",
             "values": 5000, "cm": 1},
            {"type": "liwu", "time": "2016-11-25 01:43:13", "uid": "122331", "nn": "less", "level": 13, "gfid": "飞机",
             "values": 1000, "cm": 2},
            {"type": "liwu", "time": "2016-11-25 01:45:35", "uid": "122331", "nn": "less", "level": 13, "gfid": "飞机",
             "values": 1000, "cm": 3},
            {"type": "liwu", "time": "2016-11-25 01:46:13", "uid": "122331", "nn": "less", "level": 13, "gfid": "666",
             "values": 60, "cm": 1},
            {"type": "liwu", "time": "2016-11-25 01:47:35", "uid": "122331", "nn": "less", "level": 13, "gfid": "赞",
             "values": 1, "cm": 103}
        ]
    }

    return jsonify(sdata)


# interface 7
@app.route("/zuixinxiaoxi")
@allow_cross_domain
def zuixinxiaoxi():
    rid = 0
    # rddata = {"rid": rid}
    rdata = request.get_data()

    try:
        rjson = json.loads(req)
        rid = rjson['rid']

        print rjson
    except:
        rid = 0

    sdata = {"time": "2016-11-25 14:58:03", "msg": "特别关注用户，less进入直播间"}

    return jsonify(sdata)


# interface 8
@app.route("/gongnengzhuangtai")
@allow_cross_domain
def gongnengzhuangtai():
    rid = 0
    # rddata = {"rid": rid}
    rdata = request.get_data()

    try:
        rjson = json.loads(req)
        rid = rjson['rid']

        print rjson
    except:
        rid = 0

    sdata = {
        "modify_time": "2016-11-25 14:58:03",
        "rid": rid,
        "dangmudiange": "on",
        "guanjianzitongji": "off",
        "danmuchoujiang": "off",
    }

    return jsonify(sdata)


# interface 9
@app.route("/gongnengkaiguan")
@allow_cross_domain
def gongnengkaiguan():
    rid = 0

    # rdata = {"rid": rid, "guanjianzitongji":"off",  "danmuchoujiang":"off"}
    rdata = request.get_data()

    try:
        rjson = json.loads(req)
        rid = rjson['rid']

        print rjson
    except:
        rid = 0

    sdata = {
        "modify_time": "2016-11-25 14:58:03",
        "rid": rid,
        "dangmudiange": "on",
        "guanjianzitongji": "off",
        "danmuchoujiang": "off",
    }

    return jsonify(sdata)


# interface 10

marbowzhuangtai_cnt = 0


@app.route("/marbowzhuangtai")
@allow_cross_domain
def marbowzhuangtai():
    rid = str(request.args.get('loc_id', 0))
    # rddata = {"rid": rid}
    # rdata = request.get_data()

    # try:
    #    rjson = json.loads(req)
    #    rid = rjson['rid']
    #
    #    p#rint rjson
    # except:
    #    rid = 0
    global marbowzhuangtai_cnt
    tstr = time.strftime('%y-%m-%d %H:%M:%S', time.localtime())

    global marbow, msg
    zhibojian = marbow.get_zhibojian_by_rid(rid)
    if zhibojian == None:
        sdata = {"time": tstr, "biaoqin": 1, "duration": 5, "msg": u"直播间不存在"}
        return jsonify(sdata)
    user_info = zhibojian.danmu_ctrl.uenter_info
    if user_info:
        if user_info[0]['uid'] != user_id['uid']:
            marbowzhuangtai_cnt = 1
            msg = "欢迎 %s 来到本直播间！" % user_info[0]['nn']
            user_id['uid'] = user_info[0]['uid']

            # 欢迎，郁闷，开心，一般
    if marbowzhuangtai_cnt == 1:
        biaoqin = 1
        duration = 5
    elif marbowzhuangtai_cnt == 2:
        biaoqin = 2
        duration = 5
        msg = "蓝廋，香菇"
    elif marbowzhuangtai_cnt == 3:
        biaoqin = 3
        duration = 5
        msg = "妈个蛋，今天没有面条吃"
    else:
        biaoqin = 0
        duration = 5
        msg = "一日,我上气不接下气追赶末班车，一边追一边喊：师傅!师傅等等我呀~ 车窗突然有名乘客探出头来，慢条斯理的对着我说：悟空．你就别追了"
    if marbowzhuangtai_cnt < 3:
        marbowzhuangtai_cnt += 1
    else:
        marbowzhuangtai_cnt = 0

    sdata = {"time": tstr, "biaoqin": biaoqin, "duration": duration, "msg": msg}
    print "New  message::", json.dumps(sdata, encoding='utf-8', ensure_ascii=False)
    return jsonify(sdata)


def data_init():
    onehour = datetime.timedelta(hours=1)
    onemin = datetime.timedelta(minute=1)

    period = onemin

    etime = datetime.datetime.now()
    stime = etime - onehour

    ntime = stime

    global zhuyaoshuju_records

    while ntime <= etime:
        tstr = ntime.strptime('%y-%m-%d %H:%M:%S')
        record = zhuyaoshuju_record_gen(0, tstr)
        zhuyaoshuju_records.append(record)
        ntime += period


def flask_start():
    app.run(host='0.0.0.0', threaded=True, debug=True, use_reloader=False)


if __name__ == "__main__":
    thread.start_new_thread(flask_start, ())
    marbow.cmdloop()
