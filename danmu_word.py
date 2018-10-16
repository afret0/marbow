#-*- coding: utf-8 -*-

import sys
reload(sys);
sys.setdefaultencoding('utf-8');

import time
import MySQLdb
import thread
from douyu.char import *
from danmu_talk import *
from zblib.zbroom import *

class DanmuWord(HYClass):
    print "this is danmu_word"

    def word_start(self):
        pass

    def word_stop(self):
        pass