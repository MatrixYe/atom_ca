# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         graph_demo2 
# Author:       yepeng
# Date:         2026/3/8 20:11
# Description: 
# -------------------------------------------------------------------------------

import streamlit as st
from pyvis.network import Network
import tempfile
import networkx as nx
import os
# ---------------------- 2. 交互式图可视化（PyVis + Streamlit） ----------------------
st.subheader("2. 交互式图展示（可拖拽/缩放节点）")
G = nx.DiGraph()  # 有向图
# 添加节点
input_nodes = [f"输入{i}" for i in range(1, 4)]
hidden_nodes = [f"隐藏{i}" for i in range(1, 5)]
output_nodes = [f"输出{i}" for i in range(1, 3)]
G.add_nodes_from(input_nodes, layer="input")
G.add_nodes_from(hidden_nodes, layer="hidden")
G.add_nodes_from(output_nodes, layer="output")
# 添加边（模拟节点连接）
for in_node in input_nodes:
    for hid_node in hidden_nodes[:3]:
        G.add_edge(in_node, hid_node)
for hid_node in hidden_nodes:
    for out_node in output_nodes:
        G.add_edge(hid_node, out_node)
# 用PyVis构建交互式网络
net = Network(directed=True, width="100%", height="800px", bgcolor="#f5f5f5", font_color="black")
# 加载NetworkX的图到PyVis
net.from_nx(G)
# 自定义节点样式（可选）
for node in net.nodes:
    if "输入" in node["id"]:
        node["color"] = "#87CEEB"
    elif "隐藏" in node["id"]:
        node["color"] = "#90EE90"
    else:
        node["color"] = "#FFA07A"

# 保存为临时HTML文件（Streamlit需通过HTML展示PyVis图）
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
    net.save_graph(f.name)
    with open(f.name, "r", encoding="utf-8") as f_html:
        html_content = f_html.read()
    st.components.v1.html(html_content, height=420)
os.unlink(f.name)  # 删除临时文件
