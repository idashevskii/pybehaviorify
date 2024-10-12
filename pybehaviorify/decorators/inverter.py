import pybehaviorify
from pybehaviorify.core.base import NodeStatus


class Inverter(pybehaviorify.Decorator):
    async def tick(self, tick):
        if not self.child:
            return NodeStatus.ERROR

        status = await self.child._execute(tick)

        if status == NodeStatus.SUCCESS:
            status = NodeStatus.FAILURE
        elif status == NodeStatus.FAILURE:
            status = NodeStatus.SUCCESS

        return status
