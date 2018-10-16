# -*- coding: UTF-8 -*-

from counter import HYCounter

if __name__ == '__main__':
    cnt = HYCounter("CNTTest")

    cnt.cnt_dump()
    cnt.cnt_inc("cnt0")
    cnt.cnt_dump()
    cnt.cnt_add("cnt0", 3)
    cnt.cnt_dump()
    cnt.cnt_set("cnt1", 2)
    cnt.cnt_dump()
    cnt.cnt_zero("cnt0")
    cnt.cnt_dump()
    cnt.cnt_clear()
    cnt.cnt_dump()

    cnt.cmdloop() 

    
