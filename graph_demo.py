# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         main
# Author:       yepeng
# Date:         2026/3/8 20:11
# Description:
# -------------------------------------------------------------------------------

import os
import tempfile
from dataclasses import dataclass
from typing import List

import networkx as nx
import streamlit as st
from pyvis.network import Network


@dataclass()
class User:
    atom_in: List[int]
    atom_new: List[int]
    atom_out: List[int]
    linkout: List[str]

    @classmethod
    def default(cls):
        return cls(atom_in=[],
                   atom_new=[],
                   atom_out=[],
                   linkout=[])


# 页面配置
st.set_page_config(page_title="原子计算模型可视化演示", layout="centered")
st.title("原子计算模型")

G = nx.DiGraph()
# nodes = [a for a in range(10)]
nodes = [User.default() for a in range(10)]

print(nodes)

G.add_nodes_from(nodes)
st.write(G)
net = Network(directed=True, width="100%", height="800px", bgcolor="#f5f5f5", font_color="black")
net.from_nx(G)

# 保存为临时HTML文件（Streamlit需通过HTML展示PyVis图）
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
    net.save_graph(f.name)
    with open(f.name, "r", encoding="utf-8") as f_html:
        html_content = f_html.read()
    st.components.v1.html(html_content, height=420)
os.unlink(f.name)  # 删除临时文件
