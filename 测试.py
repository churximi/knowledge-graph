#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
功能：
时间：
"""

import re


pat = re.compile("[^\u4e00-\u9fa5\w|()\n？?:（）\-/[\] ]")
f = open("/Users/simon/Mycodes/knowledge-graph/data/药物_相关文献/药物_相关文献.txt")
for line in f:
    finds = re.findall(pat, line)
    if finds:
        print(line)

f.close()
if __name__ == "__main__":
    pass
