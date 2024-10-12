import pybehaviorify
import unittest

from tests.common import NodeStub


class TestComposite(unittest.TestCase):

    async def test_initialization(self):
        ch1 = NodeStub()
        node = pybehaviorify.Decorator(child=ch1)

        self.assertIsNotNone(node.child)
        self.assertEqual(node.child, ch1)


if __name__ == "__main__":
    unittest.main()
