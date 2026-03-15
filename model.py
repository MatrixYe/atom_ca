# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         model 
# Author:       yepeng
# Date:         2026/3/8 14:38
# Description: 
# -------------------------------------------------------------------------------

from dataclasses import dataclass
from typing import List


@dataclass
class User:
    atom_in: List[int] = None
    atom_new: List[int] = None
    atom_out: List[int] = None
    linkout: List[str] = None


# 测试代码
if __name__ == "__main__":
    # 创建实例
    user1 = User()
    print("默认值测试:", user1)

    # 创建带参数的实例
    user2 = User(
        atom_in=[1, 2, 3],
        atom_new=[4, 5],
        atom_out=[6],
        linkout=["a", "b"]
    )
    print("带参数测试:", user2)
