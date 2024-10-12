import pybehaviorify
import unittest
from common import *
from pybehaviorify.core.base import NodeStatus

class TestSucceeder(unittest.TestCase):

    async def test_tick(self):
        node = pybehaviorify.Succeeder()
        status = await node._execute(TickStub())
        self.assertEqual(status, NodeStatus.SUCCESS)

if __name__ == '__main__':
    unittest.main()