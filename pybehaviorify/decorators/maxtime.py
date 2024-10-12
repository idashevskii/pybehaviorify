import pybehaviorify
import time

from pybehaviorify.core.base import NodeStatus

class MaxTime(pybehaviorify.Decorator):
    def __init__(self, child, max_time=0):
        super(MaxTime, self).__init__(child)

        self.max_time = max_time

    def open(self, tick):
        t = time.time()
        tick.blackboard.set('startTime', t, tick.tree.id, self.id)

    async def tick(self, tick):
        if not self.child:
            return NodeStatus.ERROR

        currTime = time.time();
        startTime = tick.blackboard.get('startTime', tick.tree.id, self.id);
        
        status = await self.child._execute(tick);
        if (currTime - startTime > self.max_time):
            return NodeStatus.FAILURE;
        
        return status;
        
