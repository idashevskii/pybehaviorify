import pybehaviorify
import unittest
from common import *


class TestLimiter(unittest.TestCase):

    async def test_limit(self):
        node = NodeStub()
        limiter = pybehaviorify.Limiter(node, max_loop=10)
        tick = TickStub()

        tick.blackboard.get = mock.Mock(
            side_effect=create_side_effects([False, 0, False])
        )
        await limiter._execute(tick)
        self.assertEqual(node._execute.call_count, 1)  # type: ignore

        tick.blackboard.get = mock.Mock(
            side_effect=create_side_effects([False, 10, False])
        )
        await limiter._execute(tick)
        self.assertEqual(node._execute.call_count, 1)  # type: ignore

    async def test_running_doesnt_count(self):
        node = NodeStub()
        limiter = pybehaviorify.Limiter(node, max_loop=10)
        tick = TickStub()

        tick.blackboard.get = mock.Mock(
            side_effect=create_side_effects([False, 0, False])
        )
        await limiter._execute(tick)
        self.assertEqual(node._execute.call_count, 1)  # type: ignore


if __name__ == "__main__":
    unittest.main()
