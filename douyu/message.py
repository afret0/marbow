# -*- coding: utf-8 -*-
import  json

def escape(value):
    value = str(value)
    value = value.replace("@", "@A")
    value = value.replace("/", "@S")
    return value


def unescape(value):
    value = str(value)
    value = value.replace("@S", "/")
    value = value.replace("@A", "@")
    return value


def serialize(data): #链接信息
    if data is None:
        return ''
#
    kv_pairs = []
    for key, value in data.iteritems():
        kv_pairs.append(escape(key) + "@=" + escape(value))
    kv_pairs.append('')

    result = "/".join(kv_pairs)
    # print '[Serializer] Result: %s' % result
    return result


def deserialize(raw):
    result = {}

    if raw is None or len(raw) <= 0:
        return result

    kv_pairs = raw.split("/")
    for kv_pair in kv_pairs:

        if len(kv_pair) <= 0:
            continue

        kv = kv_pair.split("@=")
        if len(kv) != 2:
            # print '[Deserialize] Invalid KV_PAIR: %s' % kv_pair
            continue

        k = unescape(kv[0])
        v = unescape(kv[1])
        if not k:
            # print '[Deserialize] Invalid KV_PAIR after unescaping: %s' % kv_pair
            continue
        if not v:
            v = ''

        # Nested deserialize
        try:
            if v.index('@=') >= 0:
                v = deserialize(v)
        except ValueError as e:
            pass

        result[k] = v

    return result


def deserialize2(raw):
    list = []

    if raw is None or len(raw) <= 0:
        return result

    kv_pairs = raw.split("/")
    for kv_pair in kv_pairs:

        result = {}
        if len(kv_pair) <= 0:
            continue

        kv_pair = unescape(kv_pair)

        # id@=70082/nr@=1/ml@=10000/ip@=danmu.douyu.com/port@=12602/

        lv_pairs = kv_pair.split("/")

        for lv_pair in lv_pairs:
            kv = lv_pair.split("@=")

            if len(kv) != 2:
                continue

            k = unescape(kv[0])
            v = unescape(kv[1])
            if not k:
                # print '[Deserialize] Invalid KV_PAIR after unescaping: %s' % kv_pair
                continue
            if not v:
                v = ''

            result[k] = v
        list.append(result)

    return list


class Message:
    def __init__(self, body):
        self.body = body
        self._serialized_size = 0

    def to_text(self):
        return serialize(self.body)

    def size(self):
        return self._serialized_size

    def attr(self, attr_name):
        #print "message:"
        #print json.dumps(self.body, encoding='utf-8', ensure_ascii=False)
        if self.body is None:
            return None
        try:
            result = self.body[attr_name]
            return result
        except KeyError as e:
            return None

    @staticmethod
    def sniff(buff):

        # print '[Message] Sniffing message'

        if buff is None or len(buff) <= 0:
            # print '[Message] Empty message buffer'
            return None

        msg_bodies = buff.split('\0')
        if len(msg_bodies) <= 1:
            # print '[Message] No messages detected'
            return None

        # print '[Message] Messages detected in buffer: Count %d' % len(msg_bodies)

        return Message.from_raw(msg_bodies[0])

    @staticmethod
    def from_raw(raw):
        result = Message(deserialize(raw))
        result._serialized_size = len(raw)
        return result
