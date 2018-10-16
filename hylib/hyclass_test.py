# -*- coding: UTF-8 -*-

from hybase import *
from hyclass import *

class HYClass_test(HYClass):
    testarg = None

    def __init__(self, modid, testarg):
        HYClass.__init__(self, modid)
        self.testarg = testarg

    def testarg_dump(self):
        print "testarg = ", self.testarg

#End of HYClass_test

if __name__ == '__main__':
    test = HYClass_test("test0", "arg0")

    test.testarg_dump()

    test.module_info_dump()

    test.dbg_flag_add("TEST", 1)

    test.dbg_info("TEST", "info")
    test.dbg_err("TEST", "error")
    test.dbg_noti("TEST", "noti")
    test.dbg_alert("TEST", "alert")
    test.dbg_warn("TEST", "warn")
    test.dbg_debug("TEST", "debug")

    modid = test.modid_get();

    print "modid = ", modid

    test.cnt_dump()
    test.cnt_inc("cnt0")
    test.cnt_dump()
    test.cnt_add("cnt0", 3)
    test.cnt_dump()
    test.cnt_set("cnt1", 2)
    test.cnt_dump()
    test.cnt_zero("cnt0")
    test.cnt_dump()

    test.cnt_clear()
    test.cnt_dump()
    
    test.cmdloop() 
