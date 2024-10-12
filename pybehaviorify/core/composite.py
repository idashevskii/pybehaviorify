from typing import List, Optional
import pybehaviorify
from pybehaviorify.core.base import BaseNode

class Composite[T](pybehaviorify.BaseNode[T]):

    def __init__(self, children: Optional[List[BaseNode[T]]] = None):
        super(Composite, self).__init__()

        self.children = children or []
