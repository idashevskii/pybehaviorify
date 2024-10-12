import pybehaviorify
from pybehaviorify.core.base import NodeStatus
from pybehaviorify.core.tick import Tick


class Succeeder(pybehaviorify.Action):
    async def tick(self, tick):
        return NodeStatus.SUCCESS
