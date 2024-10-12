import pybehaviorify
import unittest
from common import *
from pybehaviorify.core.base import NodeStatus

class TestFailer(unittest.TestCase):

    async def test_tick(self):
        node = pybehaviorify.Failer()
        status = await node._execute(TickStub())
        self.assertEqual(status, NodeStatus.FAILURE)

if __name__ == '__main__':
    unittest.main()