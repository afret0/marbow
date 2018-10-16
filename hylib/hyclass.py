#-*- coding: utf-8 -*-

import uuid

import time
import inspect

from counter import *
from debug import *
from utils import *

class HYClass(HYDebug, HYCounter, HYUtils):

    def module_info_dump(self):
        HYCounter.module_info_dump(self)
        print "  Include HYDebug, HYCounter."

#End of HYClass
