#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    Author:rendy
    Version:0.2
    E-mail:rendyqi@gmail.com
"""

import os.path
import itertools

class PinYin(object):
    def __init__(self, dict_file='pydata'):
        self.word_dict = {}
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.dict_file = os.path.join(basedir, dict_file)

    def load_dict(self):
        if not os.path.exists(self.dict_file):
            raise IOError("NotFoundFile")

        with open(self.dict_file) as f_obj:
            for f_line in f_obj.readlines():
                line = f_line.split('=')
                self.word_dict[line[0]] = line[1]

    def py_char(self, char):
        result = []
        if self.__is_chinese(char):
            key = '%X' % ord(char)
            result = self.word_dict.get(key).split()
        else:
            result.append(char)
        for i in range(len(result)):
            result[i] = result[i].lower()
        return result

    def py_string(self, string):
        result = []
        pylist = []
        for char in string:
            pys = self.py_char(char)
            pylist.append(pys)
        result = self.__py_product(pylist)
        return result

    def spy_char(self, char):
        result = []
        result = self.py_char(char)
        for i in range(len(result)):
            result[i] = result[i][0:1]
        return list(set(result))

    def spy_string(self, string):
        result = []
        pylist = []
        for char in string:
            pys = self.spy_char(char)
            pylist.append(pys)
        result = self.__py_product(pylist)
        return result

    def __py_product(self, pylist):
        result = []
        for pys in pylist:
            if len(result)>0:
                prod = itertools.product(result, pys)
                #result.clear() python 3.2不支持clear
                result = []
                for item in prod:
                    result.append(''.join(item))
            else:
                result = pys
        return result

    def __is_chinese(self, char):
        key = ord(char)
        if key>0x4e00 and key<0x9fa6:
            return True
        return False


if __name__ == "__main__":
    test = PinYin()
    test.load_dict()
    char = "参"
    string = "人参传"
    string1 = "rendy1234$%#"

    print ("char: %s" % char)
    print ("string: %s\n" % string)
    print ("py_char: %s\n" % str(test.py_char(char)))
    print ("py_string: %s\n" % str(test.py_string(string)))
    print ("spy_char: %s\n" % str(test.spy_char(char)))
    print ("spy_string: %s\n" % str(test.spy_string(string)))

    print ("py_string1: %s\n" % str(test.py_string(string1)))
