#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
功能：常用功能汇总
时间：2017年11月29日14:36:29
"""

import os
import jieba
import json


def get_lines(file_path):
    """读取文本的每一行存入list
    :param file_path:文本路径
    :return:词表list
    """
    lines = []
    with open(file_path) as f:
        for line in f:
            lines.append(line.strip())

    return lines


def get_file_paths(dir_path):
    """
    获取目录内所有指定格式的文件路径
    :param dir_path:目录路径
    :return:文件路径列表
    """
    filenames = os.listdir(dir_path)
    paths = []
    for fn in filenames:
        if fn.endswith(".txt"):  # 筛选指定格式的文本
            paths.append(os.path.abspath(os.path.join(dir_path, fn)))  # 文本绝对路径

    return paths


def create_user_dic(dir_path, seg_dict):
    """利用所有词表更新用户词典（分词用）
    :param dir_path:所有词表所在目录
    :param seg_dict:生成用户词典文本路径
    :return:字典列表
    """
    file_paths = get_file_paths(dir_path)
    out = open(seg_dict, "w+")

    words = {}
    for fp in file_paths:
        with open(fp) as f:
            for line in f:
                line = line.strip()
                if line not in words:
                    words[line] = os.path.basename(fp)
                    out.write(line + "\n")
                else:
                    pass
                    # print(line, os.path.basename(fp), words[line])  # 查看不同词表中重复的词

    out.close()

    return list(words.keys())


def update_dic():
    data_dir = "all_dics"
    seg_dict = "user_dic/用户词典.txt"
    create_user_dic(data_dir, seg_dict)  # 更新分词词典
    print("分词词典更新完成...")

    jieba.load_userdict(seg_dict)  # 加载用户词典
    print("分词词典加载完成...")


def seg_corrections(sen_words):
    """
    对分词进行修正处理
    :param sen_words:原来的分词列表
    :return:新的分词列表
    """
    incorrects = get_lines("user_dic/错分词.txt")
    dic = {}
    words = []

    for x in incorrects:
        temp = x.split("|")
        dic[temp[0]] = temp[1].split(" ")

    for word in sen_words:
        if word in dic:
            words.extend(dic[word])
        else:
            words.append(word)

    return words


def write_json(data, fpath):
    """
    将数据写入json文件
    :param data:待写入数据
    :param fpath:写入文本路径
    :return:
    """
    out = open(fpath, "w+")
    json.dump(data, out, ensure_ascii=False, indent=4)
    out.close()


def load_json(fpath):
    f = open(fpath)
    data = json.load(f)
    f.close()

    return data


if __name__ == "__main__":
    y = get_file_paths("all_dics")
    y2 = create_user_dic("all_dics", "user_dic/用户词典.txt")
    print(y2)
