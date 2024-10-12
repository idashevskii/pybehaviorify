import pybehaviorify
import unittest

from pybehaviorify.core.base import BaseNode
from pybehaviorify.core.behavior_tree import BehaviorTree
from pybehaviorify.core.blackboard import Blackboard


class TestTick(unittest.TestCase):

    async def test_initialization(self):
        tick = create_instance()

        self.assertIsNotNone(tick.tree)
        self.assertIsNone(tick.target)
        self.assertIsNotNone(tick.blackboard)
        self.assertEqual(tick._node_count, 0)
        self.assertListEqual(tick._open_nodes, [])

    async def test_updateTickOnEnter(self):
        tick = create_instance()
        node = BaseNode()

        tick._enter_node(node)

        self.assertEqual(tick._node_count, 1)
        self.assertListEqual(tick._open_nodes, [node])

    async def test_updateTickOnClose(self):
        tick = create_instance()
        node = BaseNode()

        tick._node_count = 1
        tick._open_nodes = [node]
        tick._close_node(node)

        self.assertEqual(tick._node_count, 1)
        self.assertListEqual(tick._open_nodes, [])


def create_instance():
    return pybehaviorify.Tick(blackboard=Blackboard(), tree=BehaviorTree())


if __name__ == "__main__":
    unittest.main()
