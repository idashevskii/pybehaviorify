import pybehaviorify
import unittest
from common import *
from pybehaviorify.composites.mem_selector import BB_RUNNING_CHILD
from pybehaviorify.core.base import BB_IS_OPEN, NodeStatus

def get_node(status):
    stub = NodeStub();
    stub._execute.return_value = status # type: ignore
    return stub

class TestMemPriority(unittest.TestCase):

    async def test_initialization(self):
        node = pybehaviorify.MemSelector()

        self.assertIsNotNone(node.id)
        self.assertEqual(node.name, 'MemSelector')
        self.assertEqual(node.title, 'MemSelector')
        self.assertIsNotNone(node.description)

    async def test_success(self):
        node1 = get_node(NodeStatus.FAILURE)
        node2 = get_node(NodeStatus.SUCCESS)
        node3 = get_node(NodeStatus.SUCCESS)

        mem_selector = pybehaviorify.MemSelector(children=[node1, node2, node3])
        tick = TickStub()
        tick.blackboard.get.return_value = 0 # type: ignore
        status = mem_selector.tick(tick)

        self.assertEqual(status, NodeStatus.SUCCESS)
        self.assertEqual(node1._execute.call_count, 1) # type: ignore
        self.assertEqual(node2._execute.call_count, 1) # type: ignore
        self.assertEqual(node3._execute.call_count, 0) # type: ignore

    async def test_failure(self):
        node1 = get_node(NodeStatus.FAILURE)
        node2 = get_node(NodeStatus.FAILURE)
        node3 = get_node(NodeStatus.FAILURE)

        mem_selector = pybehaviorify.MemSelector(children=[node1, node2, node3])
        tick = TickStub()
        tick.blackboard.get.return_value = 0 # type: ignore
        status = mem_selector.tick(tick)

        self.assertEqual(status, NodeStatus.FAILURE)
        self.assertEqual(node1._execute.call_count, 1) # type: ignore
        self.assertEqual(node2._execute.call_count, 1) # type: ignore
        self.assertEqual(node3._execute.call_count, 1) # type: ignore

    async def test_running(self):
        node1 = get_node(NodeStatus.FAILURE)
        node2 = get_node(NodeStatus.FAILURE)
        node3 = get_node(NodeStatus.RUNNING)
        node4 = get_node(NodeStatus.SUCCESS)

        mem_selector = pybehaviorify.MemSelector(children=[node1, node2, node3, node4])
        tick = TickStub()
        tick.blackboard.get.return_value = 0 # type: ignore
        status = mem_selector.tick(tick)

        self.assertEqual(status, NodeStatus.RUNNING)
        self.assertEqual(node1._execute.call_count, 1) # type: ignore
        self.assertEqual(node2._execute.call_count, 1) # type: ignore
        self.assertEqual(node3._execute.call_count, 1) # type: ignore
        self.assertEqual(node4._execute.call_count, 0) # type: ignore

    async def test_error(self):
        node1 = get_node(NodeStatus.FAILURE)
        node2 = get_node(NodeStatus.FAILURE)
        node3 = get_node(NodeStatus.ERROR)
        node4 = get_node(NodeStatus.SUCCESS)

        mem_selector = pybehaviorify.MemSelector(children=[node1, node2, node3, node4])
        tick = TickStub()
        tick.blackboard.get.return_value = 0 # type: ignore
        status = mem_selector.tick(tick)

        self.assertEqual(status, NodeStatus.ERROR)
        self.assertEqual(node1._execute.call_count, 1) # type: ignore
        self.assertEqual(node2._execute.call_count, 1) # type: ignore
        self.assertEqual(node3._execute.call_count, 1) # type: ignore
        self.assertEqual(node4._execute.call_count, 0) # type: ignore

    async def test_memory(self):
        node1 = get_node(NodeStatus.FAILURE)
        node2 = get_node(NodeStatus.FAILURE)
        node3 = get_node(NodeStatus.RUNNING)
        node4 = get_node(NodeStatus.SUCCESS)
        node5 = get_node(NodeStatus.FAILURE)

        mem_selector = pybehaviorify.MemSelector(children=[node1, node2, node3, node4, node5])
        mem_selector.id = 'node1';
        tick = TickStub()
        tick.blackboard.get.return_value = 0 # type: ignore
        status = await mem_selector._execute(tick)

        expected = [
            mock.call(BB_IS_OPEN, True, 'tree1', 'node1'),
            mock.call(BB_RUNNING_CHILD, 0, 'tree1', 'node1'),
            mock.call(BB_RUNNING_CHILD, 2, 'tree1', 'node1')
        ]
        result = tick.blackboard.set.mock_calls # type: ignore
        self.assertListEqual(result, expected)

    async def test_memory_continue(self):
        node1 = get_node(NodeStatus.FAILURE)
        node2 = get_node(NodeStatus.FAILURE)
        node3 = get_node(NodeStatus.FAILURE)
        node4 = get_node(NodeStatus.SUCCESS)
        node5 = get_node(NodeStatus.FAILURE)

        mem_selector = pybehaviorify.MemSelector(children=[node1, node2, node3, node4, node5])
        mem_selector.id = 'node1';
        tick = TickStub()
        tick.blackboard.get.return_value = 2 # type: ignore
        status = await mem_selector._execute(tick)

        expected = [
            mock.call(BB_IS_OPEN, False, 'tree1', 'node1'),
        ]
        result = tick.blackboard.set.mock_calls # type: ignore
        self.assertListEqual(result, expected)

        self.assertEqual(node1._execute.call_count, 0) # type: ignore
        self.assertEqual(node2._execute.call_count, 0) # type: ignore
        self.assertEqual(node3._execute.call_count, 1) # type: ignore
        self.assertEqual(node4._execute.call_count, 1) # type: ignore
        self.assertEqual(node5._execute.call_count, 0) # type: ignore



if __name__ == '__main__':
    unittest.main()