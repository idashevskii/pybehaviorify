import pybehaviorify
from pybehaviorify.core.base import NodeStatus

BB_COUNTER = "i"


class RepeatUntilSuccess(pybehaviorify.Decorator):
    def __init__(self, child, max_loop=-1):
        super(RepeatUntilSuccess, self).__init__(child)

        self.max_loop = max_loop

    def open(self, tick):
        tick.blackboard.set(BB_COUNTER, 0, tick.tree.id, self.id)

    async def tick(self, tick):
        if not self.child:
            return NodeStatus.ERROR

        i = tick.blackboard.get(BB_COUNTER, tick.tree.id, self.id)
        status = NodeStatus.SUCCESS
        while self.max_loop < 0 or i < self.max_loop:
            status = await self.child._execute(tick)

            if status == NodeStatus.FAILURE:
                i += 1
            else:
                break

        tick.blackboard.set(BB_COUNTER, i, tick.tree.id, self.id)
        return status
