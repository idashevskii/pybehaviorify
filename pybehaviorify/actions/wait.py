import pybehaviorify
import time

from pybehaviorify.core.base import NodeStatus
from pybehaviorify.core.tick import Tick

BB_START_TIME = "start_time"

class Wait(pybehaviorify.Action):
    def __init__(self, milliseconds: int = 0):
        super(Wait, self).__init__()
        self.__timeout_secs = milliseconds / 1000.0

    def open(self, tick):
        start_time = time.time()
        tick.blackboard.set(BB_START_TIME, start_time, tick.tree.id, self.id)

    async def tick(self, tick):
        curr_time = time.time()
        start_time = tick.blackboard.get(BB_START_TIME, tick.tree.id, self.id)

        if curr_time - start_time > self.__timeout_secs:
            return NodeStatus.SUCCESS

        return NodeStatus.RUNNING
