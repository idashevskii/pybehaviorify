from typing import Optional
from unittest import mock

from pybehaviorify.core.base import BaseNode
from pybehaviorify.core.blackboard import Blackboard
from pybehaviorify.core.tick import Tick


class TickStub(Tick):
    def __init__(self, blackboard: Optional[Blackboard] = None):
        self.tree = mock.Mock()
        self.blackboard = blackboard or mock.Mock()
        self._enter_node = mock.Mock()
        self._open_node = mock.Mock()
        self._tick_node = mock.Mock()
        self._close_node = mock.Mock()
        self._exit_node = mock.Mock()
        self.open_nodes = []
        self.node_count = 0

        self.tree.id = "tree1"


class NodeStub(BaseNode):
    def __init__(self):
        self._execute = mock.Mock()


def create_side_effects(results):
    def function(*args, **kwargs):
        return results.pop(0)

    return function
