import pybehaviorify
import unittest
from common import *

from unittest import mock
import time

from pybehaviorify.core.base import NodeStatus


class TestWait(unittest.TestCase):

    async def test_tick(self):
        wait = pybehaviorify.Wait(milliseconds=15)
        wait.id = "node1"

        _t = time.time()
        tick = TickStub()
        tick.blackboard.get = mock.Mock(
            side_effect=create_side_effects(
                [
                    False,  # BB_IS_OPEN inside _open
                    _t,  # start_time inside tick
                    False,  # BB_IS_OPEN inside _close
                    True,  # BB_IS_OPEN inside _open
                    _t,  # start_time inside tick
                    False,  # BB_IS_OPEN inside _close
                ]
            )
        )

        status = await wait._execute(tick)
        self.assertEqual(status, NodeStatus.RUNNING)

        while (time.time() - _t) * 1000 < 25:
            time.sleep(0.01)

        status = await wait._execute(tick)
        self.assertEqual(status, NodeStatus.SUCCESS)


if __name__ == "__main__":
    unittest.main()
