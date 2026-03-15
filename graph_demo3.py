# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         graph_demo3 
# Author:       yepeng
# Date:         2026/3/8 20:12
# Description: 
# -------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st
# ---------------------- 3. 动态演示算法步骤（图的遍历/节点更新） ----------------------
st.subheader("3. 动态演示：图节点遍历过程")


# 模拟算法步骤：遍历图的节点（比如广度优先遍历）
def bfs_step_by_step(G, start_node):
    """生成BFS遍历的每一步结果"""
    visited = []
    queue = [start_node]
    while queue:
        current = queue.pop(0)
        if current not in visited:
            visited.append(current)
            # 获取当前节点的邻居
            neighbors = list(G.neighbors(current))
            queue.extend(neighbors)
            yield visited.copy()  # 生成每一步的遍历结果


# 选择起始节点
start_node = st.selectbox("选择遍历起始节点", input_nodes + hidden_nodes + output_nodes)
start_btn = st.button("开始演示BFS遍历")

if start_btn:
    # 初始化步骤容器
    step_container = st.empty()
    progress_bar = st.progress(0)

    # 生成遍历步骤
    steps = list(bfs_step_by_step(G, start_node))
    total_steps = len(steps)

    # 逐步骤展示
    for i, step in enumerate(steps):
        with step_container.container():
            st.write(f"步骤 {i + 1}/{total_steps}：已遍历节点")
            st.write(step)

            # 实时更新图（标记已遍历节点）
            plt.figure(figsize=(8, 6))
            pos = nx.multipartite_layout(G, subset_key="layer")
            # 节点颜色：已遍历=红色，未遍历=灰色
            node_colors = ["red" if n in step else "lightgray" for n in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1500, arrows=True)
            st.pyplot(plt)

        progress_bar.progress((i + 1) / total_steps)
        # 延迟（模拟步骤间隔）
        st.empty().delay(0.5)  # Streamlit 1.28+ 支持delay，低版本可用time.sleep

st.write("---")
st.info(
    "扩展提示：可替换G为你的算法生成的图结构，修改bfs_step_by_step为你的核心算法逻辑（如图的最短路径、神经网络反向传播等）。")
