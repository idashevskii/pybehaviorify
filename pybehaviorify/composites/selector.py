import pybehaviorify
from pybehaviorify.core.base import NodeStatus


class Selector(pybehaviorify.Composite):
    def __init__(self, children=None):
        super(Selector, self).__init__(children)

    async def tick(self, tick):
        for node in self.children:
            status = await node._execute(tick)

            if status != NodeStatus.FAILURE:
                return status

        return NodeStatus.FAILURE
