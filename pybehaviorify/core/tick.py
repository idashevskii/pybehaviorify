from typing import List, Optional, TYPE_CHECKING

from pybehaviorify.core.blackboard import Blackboard

if TYPE_CHECKING:
    from pybehaviorify.core.behavior_tree import BehaviorTree
    from pybehaviorify.core.base import BaseNode


class Tick[T]:
    """Tick Class.

    A new Tick object is instantiated every tick by BehaviorTree. It is passed
    as parameter to the nodes through the tree during the traversal.

    The role of the Tick class is to store the instances of tree, target
    and blackboard. So, all nodes can access these informations.

    For internal uses, the Tick also is useful to store the open node after the
    tick signal, in order to let `BehaviorTree` to keep track and close them
    when necessary.
    """

    def __init__(
        self,
        blackboard: Blackboard,
        tree: "BehaviorTree",
        target: Optional[T] = None,
    ):
        """Constructor.

        :param tree: a BehaviorTree instance.
        :param target: a target object.
        :param blackboard: a Blackboard instance.
        """
        self.tree = tree
        self.target = target
        self.blackboard = blackboard

        self._open_nodes: List["BaseNode"] = []
        self._node_count: int = 0

    def _enter_node(self, node: "BaseNode"):
        """Called when entering a node (called by BaseNode).

        :param node: a node instance.
        """
        self._node_count += 1
        self._open_nodes.append(node)

    def _open_node(self, node: "BaseNode"):
        """Called when opening a node (called by BaseNode).

        :param node: a node instance.
        """
        pass

    def _tick_node(self, node: "BaseNode"):
        """Called when ticking a node (called by BaseNode).

        :param node: a node instance.
        """
        pass

    def _close_node(self, node: "BaseNode"):
        """Called when closing a node (called by BaseNode).

        :param node: a node instance.
        """
        self._open_nodes.pop()

    def _exit_node(self, node: "BaseNode"):
        """Called when exiting a node (called by BaseNode).

        :param node: a node instance.
        """
        self._node_count -= 1
