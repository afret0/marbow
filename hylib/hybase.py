#-*- coding: utf-8 -*-

import sys

from  cmd import Cmd

MAJOR_VERSION=1
MINOR_VERSION=0
AUTHOR="less"
EMAIL="less@beescast.com"
COPYRIGHT="Copyright 2016-2020 by WuHang Bees Technologes Ltd. "

E_SUCCESS = 0
E_ERROR   = 1
E_EXSIT   = 2
E_KEY     = 3

class HYBase(Cmd):
    version = "%d.%.2d" % (MAJOR_VERSION, MINOR_VERSION)
    modid = None
    author = AUTHOR
    email = EMAIL
    copyright = COPYRIGHT

    def __init__(self, modid):
        Cmd.__init__(self)
        self.modid = modid
        self.use_rawinput = 0

    def modid_get(self):
        return self.modid

    def version_get(self):
        return self.version

    def author_get(self):
        return self.author

    def email_get(self):
        return self.email

    def copyright_get(self):
        return self.copyright

    def module_info_dump(self):
        print "  %s V%s" % (self.modid, self.version)
        print "  author: ", self.author
        print "  email:  ", self.email
        print " ", self.copyright

    def err_string(self, err):
        if E_SUCCESS == err:
            return "SUCCESS"
        elif E_ERROR == err:
            return "ERROR"
        elif E_EXSIT == err:
            return "EXSIT"
        else:
            return "UNKOWN"

    def help_version(self):
        ''' help version information '''
        print "  show version information"

    def do_version(self, line):
        self.module_info_dump()

    def help_quit(self):  # 以help_*开头的为帮助
        ''' help quit information '''
        print "  Quit program"

    def do_quit(self, line):  # 以do_*开头为命令
        ''' do quit information '''
        print("Exit now ...")
        return True
        #sys.exit()

#End of file
