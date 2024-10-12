import pybehaviorify
import unittest
from common import *
from pybehaviorify.core.base import NodeStatus

class TestError(unittest.TestCase):

    async def test_tick(self):
        node = pybehaviorify.Error()
        status = await node._execute(TickStub())
        self.assertEqual(status, NodeStatus.ERROR)

if __name__ == '__main__':
    unittest.main()