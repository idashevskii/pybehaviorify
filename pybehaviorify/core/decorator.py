from typing import Optional
import pybehaviorify
from pybehaviorify.core.base import BaseNode


class Decorator[T](pybehaviorify.BaseNode[T]):

    def __init__(self, child: Optional[BaseNode[T]] = None):
        super(Decorator, self).__init__()

        self.child = child
