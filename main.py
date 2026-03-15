import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Set, Dict, List, Optional


@dataclass
class User:
    atom_in: Set[int] = field(default_factory=set)
    atom_new: Set[int] = field(default_factory=set)
    atom_out: Set[int] = field(default_factory=set)
    linkout: Set[str] = field(default_factory=set)

    def add_atom(self, atom: int, is_origin: bool):
        """
         为用户添加原子，并根据规则决定是否传播

         Args:
             atom: 原子值
             is_origin: 是否为原点原子
         """

        # 避免重复添加
        if atom in self.atom_in or atom in self.atom_new:
            return

        # 原始原子加入atom_in和atom_out
        if is_origin:
            self.atom_in.add(atom)
            self.atom_out.add(atom)
            return

        # 零原子加入atom_in,不加入atom_out
        if atom == 0:
            self.atom_in.add(atom)
            return

        # 普通原子先加入atom_in，再判断是否需要流转
        self.atom_new.add(atom)

        # 当atom_new有2个以上原子或atom_out为空时，随机选择一个流转
        if len(self.atom_new) >= 2 or len(self.atom_out) == 0:
            if not self.atom_new:
                return

            # 随机选择一个流转
            selected_atom = random.choice(list(self.atom_new))
            self.atom_out.add(selected_atom)

            # 合并atom_new到atom_in
            self.atom_in = self.atom_in | self.atom_new

            # 清空atom_new缓存
            self.atom_new.clear()


class MockDatabase:
    """
    模拟数据库，存储用户原子状态
    """

    def __init__(self):
        self._users: Dict[str, User] = {}

    def read_user(self, user_hash) -> User:
        """
        读取用户对象

        :param user_hash: 用户哈希值
        :type user_hash: str
        :return: 用户对象
        :rtype: User
        """
        return self._users.get(user_hash, None)

    def write_user(self, user_hash: str, user: User) -> bool:
        """
        写入用户对象

        :param user_hash: 用户哈希值
        :type user_hash: str
        :param user: 用户对象
        :type user: User
        :return: 是否写入成功
        :rtype: bool
        """
        # noinspection PyBroadException
        try:
            self._users[user_hash] = user
            return True
        except Exception:
            return False

    def user_exists(self, user_hash: str) -> bool:
        """
        检查用户是否存在

        :param user_hash: 用户哈希值
        :type user_hash: str
        :return: 是否存在
        :rtype: bool
        """
        return user_hash in self._users


users = {
    'user_a': User(),
    'user_b': User(),
    'user_c': User(),
    'user_d': User(),
    'user_e': User(),
    'user_f': User(),
    'user_g': User(),
    'user_h': User(),
    'user_i': User(),
    'user_j': User(),
}


def add_atoms_and_propagate(user_hash_start: str, atoms: List[int], is_origin: bool,
                            database: Optional[MockDatabase] = None):
    """
    为用户添加原子并传播

    :param user_hash_start: 起始用户哈希值
    :type user_hash_start: str
    :param atoms: 原子列表
    :type atoms: List[int]
    :param is_origin: 是否为原点原子
    :type is_origin: bool
    :param database: 数据库实例
    :type database: Optional[MockDatabase]
    :return: 是否成功
    :rtype: bool
    """
    # 使用提供的数据库或创建新的模拟数据库
    db = database or MockDatabase()

    # 创建双向队列
    # propagate_queues = [{}, {}]

    propagate_queues: List[Dict[str, List[int]]] = [defaultdict(list), defaultdict(list)]

    propagate_queues[0][user_hash_start] = atoms

    side = 0
    while propagate_queues[side]:
        print(f"is_origin: {is_origin}")
        # 当前轮次的队列和下一轮次的队列
        current_queue = propagate_queues[side]
        next_queue = propagate_queues[1 - side]

        for user_hash, received_atoms in current_queue.items():
            user = db.read_user(user_hash)

            # 如果用户不存在，创建新用户,实际上在接收review时就已经构建连接了
            if user is None:
                user = User()
                # 写入新用户到数据库
                if not db.write_user(user_hash, user):
                    return False

            # 记录原子数量变化，用于判断是否需要写入数据库
            original_in_size = len(user.atom_in)
            original_new_size = len(user.atom_new)
            original_out_size = len(user.atom_out)

            # 记录当前轮次的atom_out，用于判断是否有新地待传播原子
            original_out = user.atom_out.copy()

            # 为用户添加原子
            for atom in received_atoms:
                user.add_atom(atom, is_origin)

            # 如果是原点原子，流转一次后自动降级为普通原子
            is_origin = False

            # 如果原子数量没有变更，跳过写入数据库
            if len(user.atom_in) == original_in_size and len(user.atom_new) == original_new_size:
                continue

            # 通过新旧atom_out的差，检查是否有新地待传播原子
            if len(user.atom_out) > original_out_size:
                # new_atoms = list(user.atom_out - set(user.atom_out)[:original_out_size])
                new_atoms = list(user.atom_out - original_out)

                # 加入下一轮次的队列
                for linked_user_hash in user.linkout:
                    next_queue[linked_user_hash].extend(new_atoms)

                # 写入用户到数据库
                if not db.write_user(user_hash, user):
                    return False

        # 清空当前队列，等待下一次传播
        current_queue.clear()
        side = 1 - side

    return True


def add_atoms_and_propagate_v2(user_hash_start: str, atoms: List[int], is_origin: bool,
                               database: Optional[MockDatabase] = None):
    """
    为用户添加原子并传播(python优化版)

    :param user_hash_start: 起始用户哈希值
    :type user_hash_start: str
    :param atoms: 原子列表
    :type atoms: List[int]
    :param is_origin: 是否为原点原子
    :type is_origin: bool
    :param database: 数据库实例
    :type database: Optional[MockDatabase]
    :return: 是否成功
    :rtype: bool
    """
    print(f"add_atoms_and_propagate_v2: {user_hash_start}, {atoms}, {is_origin}")
    db = database or MockDatabase()

    # 使用集合存储待传播的用户和原子
    current_propagation: Dict[str, Set[int]] = {user_hash_start: set(atoms)}
    next_propagation: Dict[str, Set[int]] = {}

    while current_propagation:
        next_propagation.clear()

        for user_hash, received_atoms in current_propagation.items():
            user = db.read_user(user_hash)

            if user is None:
                user = User()
                if not db.write_user(user_hash, user):
                    return False

            # 记录原始状态
            original_in = user.atom_in.copy()
            original_new = user.atom_new.copy()
            original_out = user.atom_out.copy()

            # 添加原子
            for atom in received_atoms:
                user.add_atom(atom, is_origin)

            is_origin = False

            # 检查是否有变化
            if user.atom_in == original_in and user.atom_new == original_new:
                continue

            # 检查是否有新的待传播原子
            new_out_atoms = user.atom_out - original_out
            if new_out_atoms:
                # 传播给关联用户
                for linked_hash in user.linkout:
                    if linked_hash not in next_propagation:
                        next_propagation[linked_hash] = set()
                    next_propagation[linked_hash].update(new_out_atoms)

            # 写入数据库
            if not db.write_user(user_hash, user):
                return False

        # 切换传播队列
        current_propagation = next_propagation.copy()

    return True


if __name__ == '__main__':
    pass
    # 创建模拟数据库
    db = MockDatabase()

    # 创建测试用户
    user_a = User(atom_in={10, 20}, atom_out={50, 60, 70}, linkout={"user_b", "user_c"})
    user_b = User(atom_in={30}, atom_out={40}, linkout={"user_d"})
    user_c = User(atom_in=set(), atom_out=set[int](), linkout=set())
    user_d = User(atom_in=set(), atom_out=set[int](), linkout=set())

    # 写入用户数据
    db.write_user("user_a", user_a)
    db.write_user("user_b", user_b)
    db.write_user("user_c", user_c)
    db.write_user("user_d", user_d)

    # 模拟User A评论User B，触发原子传播
    success = add_atoms_and_propagate(
        user_hash_start="user_b", atoms=[50, 60, 70], is_origin=True, database=db
    )

    print(f"传播操作{'成功' if success else '失败'}")

    # 查看传播结果
    print("\n传播后的用户状态：")
    for user_hash in ["user_a", "user_b", "user_c", "user_d"]:
        user = db.read_user(user_hash)
        if user:
            print(f"{user_hash}:")
            print(f"  atom_in: {user.atom_in}")
            print(f"  atom_new: {user.atom_new}")
            print(f"  atom_out: {user.atom_out}")
            print(f"  linkout: {user.linkout}")
