import pybehaviorify
import unittest
from common import *
from pybehaviorify.core.base import NodeStatus

def get_node(status):
    stub = NodeStub();
    stub._execute.return_value = status # type: ignore
    return stub

class TestSequence(unittest.TestCase):

    async def test_initialization(self):
        node = pybehaviorify.Sequence()

        self.assertIsNotNone(node.id)
        self.assertEqual(node.name, 'Sequence')
        self.assertEqual(node.title, 'Sequence')
        self.assertIsNotNone(node.description)

    async def test_success(self):
        node1 = get_node(NodeStatus.SUCCESS)
        node2 = get_node(NodeStatus.SUCCESS)
        node3 = get_node(NodeStatus.SUCCESS)

        sequence = pybehaviorify.Sequence(children=[node1, node2, node3])
        status = sequence.tick(TickStub())

        self.assertEqual(status, NodeStatus.SUCCESS)
        self.assertEqual(node1._execute.call_count, 1) # type: ignore
        self.assertEqual(node2._execute.call_count, 1) # type: ignore
        self.assertEqual(node3._execute.call_count, 1) # type: ignore

    async def test_failure(self):
        node1 = get_node(NodeStatus.SUCCESS)
        node2 = get_node(NodeStatus.SUCCESS)
        node3 = get_node(NodeStatus.FAILURE)
        node4 = get_node(NodeStatus.SUCCESS)

        sequence = pybehaviorify.Sequence(children=[node1, node2, node3, node4])
        status = sequence.tick(TickStub())

        self.assertEqual(status, NodeStatus.FAILURE)
        self.assertEqual(node1._execute.call_count, 1) # type: ignore
        self.assertEqual(node2._execute.call_count, 1) # type: ignore
        self.assertEqual(node3._execute.call_count, 1) # type: ignore
        self.assertEqual(node4._execute.call_count, 0) # type: ignore

    async def test_running(self):
        node1 = get_node(NodeStatus.SUCCESS)
        node2 = get_node(NodeStatus.SUCCESS)
        node3 = get_node(NodeStatus.RUNNING)
        node4 = get_node(NodeStatus.SUCCESS)

        sequence = pybehaviorify.Sequence(children=[node1, node2, node3, node4])
        status = sequence.tick(TickStub())

        self.assertEqual(status, NodeStatus.RUNNING)
        self.assertEqual(node1._execute.call_count, 1) # type: ignore
        self.assertEqual(node2._execute.call_count, 1) # type: ignore
        self.assertEqual(node3._execute.call_count, 1) # type: ignore
        self.assertEqual(node4._execute.call_count, 0) # type: ignore

    async def test_error(self):
        node1 = get_node(NodeStatus.SUCCESS)
        node2 = get_node(NodeStatus.SUCCESS)
        node3 = get_node(NodeStatus.ERROR)
        node4 = get_node(NodeStatus.SUCCESS)

        sequence = pybehaviorify.Sequence(children=[node1, node2, node3, node4])
        status = sequence.tick(TickStub())

        self.assertEqual(status, NodeStatus.ERROR)
        self.assertEqual(node1._execute.call_count, 1) # type: ignore
        self.assertEqual(node2._execute.call_count, 1) # type: ignore
        self.assertEqual(node3._execute.call_count, 1) # type: ignore
        self.assertEqual(node4._execute.call_count, 0) # type: ignore


if __name__ == '__main__':
    unittest.main()