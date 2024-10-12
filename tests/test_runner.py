import pybehaviorify
import unittest
from common import *
from pybehaviorify.core.base import NodeStatus

class TestRunner(unittest.TestCase):

    async def test_tick(self):
        node = pybehaviorify.Runner()
        status = await node._execute(TickStub())
        self.assertEqual(status, NodeStatus.RUNNING)

if __name__ == '__main__':
    unittest.main()