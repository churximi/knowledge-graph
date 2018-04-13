#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
功能：远程dse操作
时间：2018年04月13日14:11:14
更新：写成类
"""

import os
import re
from dse.cluster import Cluster, GraphExecutionProfile
from dse.cluster import EXEC_PROFILE_GRAPH_DEFAULT, EXEC_PROFILE_GRAPH_SYSTEM_DEFAULT
from dse.graph import GraphOptions


class remote_dse:
    """远程dse"""

    def __init__(self):
        self.use_schema = True  # 选择是否加载schema
        self.use_data = True  # 选择是否加载数据
        self.graph_name = "medicine_03"
        self.schema_path = "0412/schema.groovy"
        self.data_path = "0412/load.groovy"
        self.address = "192.168.2.4"
        self.dse_path = os.path.join(os.environ['HOME'], "dse")  # dse路径
        self.graphloader = os.path.join(self.dse_path, "dse-graph-loader/graphloader")  # graph-loader路径

        self.load_schema(self.use_schema)
        self.load_data(self.use_data)

        print('访问查看："http://{}:9091/"'.format(self.address))

    def create_graph(self):
        # 创建默认的执行配置，指向特定的graph
        ep = GraphExecutionProfile(graph_options=GraphOptions(graph_name=self.graph_name))
        cluster = Cluster(contact_points=[self.address],
                          execution_profiles={EXEC_PROFILE_GRAPH_DEFAULT: ep})

        session = cluster.connect()

        # 创建graph
        session.execute_graph("system.graph(name).ifNotExists().create()", {'name': self.graph_name},
                              execution_profile=EXEC_PROFILE_GRAPH_SYSTEM_DEFAULT)

    def load_schema(self, use_schema=False):
        """加载schema文件
        """
        if use_schema:
            # 创建默认的执行配置，指向特定的graph
            ep = GraphExecutionProfile(graph_options=GraphOptions(graph_name=self.graph_name))
            cluster = Cluster(contact_points=[self.address],
                              execution_profiles={EXEC_PROFILE_GRAPH_DEFAULT: ep})
            session = cluster.connect()

            # 创建graph
            session.execute_graph("system.graph(name).ifNotExists().create()", {'name': self.graph_name},
                                  execution_profile=EXEC_PROFILE_GRAPH_SYSTEM_DEFAULT)

            # 批量执行gremlin创建schema的命令
            with open(self.schema_path) as f:
                pat = re.compile("[/ \n]")  # 正则表达式
                for line in f:
                    if not re.match(pat, line):  # 开头不是斜杠、空格、换行的
                        print("正在加载 {}".format(line.strip()))
                        session.execute_graph(line.strip())
        else:
            print("schema未加载，请确保graph中存在schema")

    def load_data(self, use_data=False):
        if use_data:
            print("载入数据...")
            os.system("{} {} -graph {} -address {}".format(self.graphloader, self.data_path,
                                                           self.graph_name, self.address))
            print("载入数据完成。\n")


dse = remote_dse()

if __name__ == "__main__":
    pass
