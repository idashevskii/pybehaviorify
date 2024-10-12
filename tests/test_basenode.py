from typing import cast
import unittest
from unittest import mock

from common import *

import pybehaviorify
from pybehaviorify.core.base import BB_IS_OPEN, NodeStatus


class TestBaseNode(unittest.TestCase):
    async def test_initialization(self):
        node = pybehaviorify.BaseNode()

        self.assertIsNotNone(node.id)
        self.assertIsNotNone(node.title)
        self.assertEqual(node.description, "")
        self.assertDictEqual(node.properties, {})
        self.assertEqual(node.description, "")
        self.assertRaises(AttributeError, lambda: getattr(node, "children"))
        self.assertRaises(AttributeError, lambda: getattr(node, "child"))

    async def test_openNode(self):
        node = pybehaviorify.BaseNode()
        tick = TickStub()

        node.id = "node1"

        # mocking
        tick.blackboard.get.return_value = False # type: ignore
        node._tick = mock.Mock()
        node._tick.return_value = NodeStatus.RUNNING  # does not close the node

        # run
        await node._execute(tick)

        # test
        expected = [mock.call.blackboard.set(BB_IS_OPEN, True, "tree1", "node1")]
        result = tick.blackboard.set.mock_calls # type: ignore

        self.assertListEqual(result, expected)

    async def test_closeNode(self):
        node = pybehaviorify.BaseNode()
        tick = TickStub()
        bb_mock_get = cast(mock.Mock, tick.blackboard.get)
        bb_mock_set = cast(mock.Mock, tick.blackboard.set)

        node.id = "node1"

        # mocking
        bb_mock_get.return_value = True
        node._tick = mock.Mock()
        node._tick.return_value = NodeStatus.SUCCESS  # close the node

        # run
        await node._execute(tick)

        # test
        expected = [mock.call.blackboard.set(BB_IS_OPEN, False, "tree1", "node1")]
        result = bb_mock_set.mock_calls

        self.assertListEqual(result, expected)

    async def test_executeCallingFunction(self):
        node = pybehaviorify.BaseNode()
        tick = TickStub(blackboard=Blackboard())

        node.id = "node1"

        # mocking
        node.enter = mock.Mock()
        node.open = mock.Mock()
        node.tick = mock.Mock()
        node.tick.return_value = NodeStatus.SUCCESS  # close the node
        node.close = mock.Mock()
        node.exit = mock.Mock()

        # run
        status = await node._execute(tick)

        # test
        self.assertIsNotNone(status)
        node.enter.assert_called_once_with(tick)
        node.open.assert_called_once_with(tick)
        node.tick.assert_called_once_with(tick)
        node.close.assert_called_once_with(tick)
        node.exit.assert_called_once_with(tick)

    async def test_executeDoesNotOpen(self):
        node = pybehaviorify.BaseNode()
        tick = TickStub()

        node.id = "node1"

        # mocking
        tick.blackboard.get.return_value = True # type: ignore
        node._tick = mock.Mock()
        node._tick.return_value = NodeStatus.RUNNING  # does not close the node

        # run
        await node._execute(tick)

        # test
        expected = []
        result = tick.blackboard.set.mock_calls # type: ignore

        self.assertListEqual(result, expected)

    async def test_executeCallingTickCallbacks(self):
        node = pybehaviorify.BaseNode()
        tick = TickStub(blackboard=Blackboard())

        node.id = "node1"

        # mocking
        node.tick = mock.Mock()
        node.tick.return_value = NodeStatus.SUCCESS  # close the node

        # run
        await node._execute(tick)

        cast(mock.Mock, tick._enter_node).assert_called_once_with(node)
        cast(mock.Mock, tick._open_node).assert_called_once_with(node)
        cast(mock.Mock, tick._tick_node).assert_called_once_with(node)
        cast(mock.Mock, tick._close_node).assert_called_once_with(node)
        cast(mock.Mock, tick._exit_node).assert_called_once_with(node)


if __name__ == "__main__":
    unittest.main()
