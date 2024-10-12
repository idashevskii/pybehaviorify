from pybehaviorify.core.action import Action
from pybehaviorify.core.base import NodeStatus
from pybehaviorify.core.tick import Tick


class Error(Action):
    async def tick(self, tick):
        return NodeStatus.ERROR
