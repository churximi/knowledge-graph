#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
功能：数据预处理
时间：2018年04月17日09:15:17
"""

from utils import load_json


def str_replace(string):
    return string.strip().replace("|", "/")


def format_conv():
    """将原始数据转为知识图谱load格式"""
    data = load_json("data_temp/参考文献.json")
    med_doc = open("data/药物_相关文献/药物_相关文献.txt", "w+")  # 药物-文献关系
    docs = open("data/相关文献节点/相关文献.txt", "w+")  # 参考文献节点

    med_record = dict()  # 记录药物文献数，以便编号
    for d in data:
        title, medicine = str_replace(d["title"]), str_replace(d["medicine"])
        content, other = str_replace(d["content"]), str_replace(d["other"])
        url = str_replace(d["url"])

        if medicine not in med_record:
            med_record[medicine] = 0
        med_record[medicine] += 1
        doc_id = "{}_{}".format(medicine, med_record[medicine])

        docs.write("{}|{}|{}|{}|{}|{}\n".format(doc_id, title, medicine, content, other, url))
        med_doc.write("{}|{}\n".format(medicine, doc_id))
    med_doc.close()
    docs.close()


format_conv()
if __name__ == "__main__":
    pass
