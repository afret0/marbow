#-*- coding: utf-8 -*-

from hybase import *

import json
import os

class HYUtils(HYBase):
    def json_file_load(self, filename):

        #os.chdir("../douyu/")
        #print os.getcwd()
        f = file(filename)
        d = json.load(f)

        return d

    def help_json(self):
        print "  json FILE"

    def do_json(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 1:
            return self.help_json()

        filename = argv[0]

        d = self.json_file_load(filename)

        for k in d:
            print "%25s: %s" % (k, d[k])

#Utils
if __name__ == '__main__':
    Utils = HYUtils("UTILS")
    Utils.cmdloop()