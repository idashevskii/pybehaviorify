import pybehaviorify
import unittest

from tests.common import NodeStub

class TestComposite(unittest.TestCase):

    async def test_initialization(self):
        ch1=NodeStub()
        ch2=NodeStub()
        node = pybehaviorify.Composite(children=[ch1, ch2])

        self.assertIsNotNone(node.children)
        self.assertEqual(node.children[0], ch1)
        self.assertEqual(node.children[1], ch2)

if __name__ == '__main__':
    unittest.main()