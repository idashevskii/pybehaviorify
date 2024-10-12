import pybehaviorify
import unittest
from common import *
from pybehaviorify.core.base import NodeStatus

class TestInverter(unittest.TestCase):

    async def test_success(self):
        node = NodeStub()
        inverter = pybehaviorify.Inverter(node)
        tick = TickStub()

        node._execute.return_value = NodeStatus.SUCCESS # type: ignore
        status = await inverter._execute(tick)
        self.assertEqual(status, NodeStatus.FAILURE)

    async def test_failure(self):
        node = NodeStub()
        inverter = pybehaviorify.Inverter(node)
        tick = TickStub()

        node._execute.return_value = NodeStatus.FAILURE # type: ignore
        status = await inverter._execute(tick)
        self.assertEqual(status, NodeStatus.SUCCESS)

    async def test_running(self):
        node = NodeStub()
        inverter = pybehaviorify.Inverter(node)
        tick = TickStub()

        node._execute.return_value = NodeStatus.RUNNING # type: ignore
        status = await inverter._execute(tick)
        self.assertEqual(status, NodeStatus.RUNNING)

    async def test_running_err(self):
        inverter = pybehaviorify.Inverter()
        tick = TickStub()

        status = await inverter._execute(tick)
        self.assertEqual(status, NodeStatus.ERROR)


if __name__ == '__main__':
    unittest.main()