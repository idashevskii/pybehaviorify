import pybehaviorify
from pybehaviorify.core.base import BaseNode, NodeStatus

BB_COUNTER = "i"


class Limiter(pybehaviorify.Decorator):
    def __init__(self, child: BaseNode, max_loop: int):
        super(Limiter, self).__init__(child)

        self.max_loop = max_loop

    def open(self, tick):
        tick.blackboard.set(BB_COUNTER, 0, tick.tree.id, self.id)

    async def tick(self, tick):
        if not self.child:
            return NodeStatus.ERROR

        i = tick.blackboard.get(BB_COUNTER, tick.tree.id, self.id)
        if i < self.max_loop:
            status = await self.child._execute(tick)

            if status == NodeStatus.SUCCESS or status == NodeStatus.FAILURE:
                tick.blackboard.set(BB_COUNTER, i + 1, tick.tree.id, self.id)

            return status

        return NodeStatus.FAILURE
