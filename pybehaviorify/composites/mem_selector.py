import pybehaviorify
from pybehaviorify.core.base import NodeStatus

BB_RUNNING_CHILD = "running_child"


class MemSelector(pybehaviorify.Composite):
    def __init__(self, children=None):
        super(MemSelector, self).__init__(children)

    def open(self, tick):
        tick.blackboard.set(BB_RUNNING_CHILD, 0, tick.tree.id, self.id)

    async def tick(self, tick):
        idx = tick.blackboard.get(BB_RUNNING_CHILD, tick.tree.id, self.id)

        for i in range(idx, len(self.children)):
            node = self.children[i]
            status = await node._execute(tick)

            if status != NodeStatus.FAILURE:
                if status == NodeStatus.RUNNING:
                    tick.blackboard.set(BB_RUNNING_CHILD, i, tick.tree.id, self.id)
                return status

        return NodeStatus.FAILURE
