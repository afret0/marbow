import time
from hylib.hyclass import *
from douyu.char import *

class Shuiyou(HYClass):
    def __init__(self, modid):
        #Char.__init__(self,modid)

        self.dbg_flag_add("SYOU", 1)
        self.danmu_records = []
        self.gift_records  = []
        self.enter_time =  time.time()
        self.gifts_total = 0

    def danmu_insert(self, danmu):
        self.danmu_list.insert(0, danmu)

    def gifts_insert(self, gift):
        value = douyu.gift_value(gift)
        self.gifts_total += value
        self.gifts_list.insert(0, gift)

    def gifts_total(self):
        return self.gifts_total

    def danmu_list(self):
        return self.danmu_list

    def gifts_list(self):
        return self.gifts_list

    def suiyou_start(self):
        pass

    