#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import jieba

from hylib.hyclass import	*

class Segment(HYClass):
    def __init__(self, modid):
        HYClass.__init__(self, modid)

        self.dbg_flag_add("SEG", 1)

    def wordcut(self, sentence):
        words = jieba.cut(sentence)
        self.dbg_debug("SEG", words)
        return list(words)

    def help_wordcut(self):
        print    "	 wordcut SENTENCE"
        print    u"			 ----	切词"

    def do_wordcut(self, line):
        argv = line.split()
        argc = len(argv)

        if argc != 1:
            self.help_wordcut()

        sentence = argv[0]

        words = self.wordcut(sentence)

        if words:
            #print "words: ", words
            num = len(words)
            print "切成了%d个词语:" %(num)
            for i in range(0, num):
                print "%.2d: %s" % (i, words[i])
        else:
            print    u"切词失败！"

if __name__	== "__main__":
    seg = Segment("SEG")
    seg.cmdloop()
