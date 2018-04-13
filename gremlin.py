#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
功能：本地dse操作
时间：2018年04月13日15:27:26
更新：写成类
"""

import os
import re
import time
from dse.cluster import Cluster, GraphExecutionProfile
from dse.cluster import EXEC_PROFILE_GRAPH_DEFAULT, EXEC_PROFILE_GRAPH_SYSTEM_DEFAULT
from dse.graph import GraphOptions


class local_dse:
    """本地dse"""

    def __init__(self):
        self.use_schema = True  # 选择是否加载schema
        self.use_data = True  # 选择是否加载数据
        self.graph_name = "medicine"
        self.schema_path = "0412/schema.groovy"  # schema
        self.data_path = "0412/load.groovy"  # data
        self.address = "127.0.0.1"
        self.dse_path = os.path.join(os.environ['HOME'], "dse")  # dse路径
        self.graphloader = os.path.join(self.dse_path, "dse-graph-loader/graphloader")  # graph-loader路径

        self.run_dse()
        self.run_studio()
        self.load_schema(self.use_schema)
        self.load_data(self.use_data)

        print('访问查看："http://{}:9091/"'.format(self.address))

    def get_content(self):
        """获取启动信息"""
        command = os.path.join(self.dse_path, "bin/nodetool status")
        process = os.popen(command)
        con = process.read()
        process.close()
        return con

    def run_dse(self):
        """确认DSE是否已经运行，如果没有则自动启动。
        """
        print("检查DSE是否运行...")
        information = "Datacenter"
        content = self.get_content()
        if information not in content:
            print("正在启动DSE...")
            os.system(os.path.join(self.dse_path, "bin/dse cassandra"))  # 启动DSE
            time.sleep(5)

            while information not in content:  # 重复检查启动状态
                time.sleep(5)
                content = self.get_content()
        time.sleep(5)

        print(self.get_content())
        print("**********\nOK，DSE已经运行。\n**********")

    def run_studio(self):
        command = os.path.join(self.dse_path, "datastax-studio/bin/start_studio_server")
        print("启动Datastax studio...")
        os.system(command)
        time.sleep(10)
        print("Datastax studio已启动...")
        print('访问查看："http://{}:9091/"'.format(self.address))

    def load_schema(self, use_schema=False):
        """加载schema文件
        """
        if use_schema:
            # 创建默认的执行配置，指向特定的graph
            ep = GraphExecutionProfile(graph_options=GraphOptions(graph_name=self.graph_name))
            cluster = Cluster(execution_profiles={EXEC_PROFILE_GRAPH_DEFAULT: ep})

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
        """利用DSE graphloader载入文本数据
        """
        if use_data:
            print("载入数据...")
            os.system("{} {} -graph {} -address {}".format(self.graphloader, self.data_path,
                                                           self.graph_name, self.address))
            print("载入数据完成。\n")


dse = local_dse()

if __name__ == "__main__":
    pass
