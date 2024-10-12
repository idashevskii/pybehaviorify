import pybehaviorify
from pybehaviorify.core.base import NodeStatus
from pybehaviorify.core.tick import Tick


class Sequence(pybehaviorify.Composite):

    def __init__(self, children=None):
        super(Sequence, self).__init__(children)

    async def tick(self, tick):
        for node in self.children:
            status = await node._execute(tick)

            if status != NodeStatus.SUCCESS:
                return status

        return NodeStatus.SUCCESS
