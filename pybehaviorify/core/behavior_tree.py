from typing import Optional
import pybehaviorify
import uuid
from pybehaviorify.core.base import BaseNode
from pybehaviorify.core.blackboard import Blackboard

# from pybehaviorify.core.composite import Composite
# from pybehaviorify.core.decorator import Decorator


class BehaviorTree[T]:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.title = __class__.__name__
        self.description = ""
        self.properties = {}
        self.root: Optional[BaseNode[T]] = None

    # def load(self, data, names=None):
    #     names = names or {}
    #     self.title = data["title"] or self.title
    #     self.description = data["description"] or self.description
    #     self.properties = data["properties"] or self.properties

    #     nodes = {}
    #     for key in data["nodes"]:
    #         spec = data["nodes"][key]

    #         if spec["name"] in names:
    #             cls = names[spec["name"]]

    #         elif hasattr(pybehaviorify, spec["name"]):
    #             cls = getattr(pybehaviorify, spec["name"])
    #         else:
    #             raise RuntimeError(
    #                 'BehaviorTree.load: Invalid node name "%s"' % spec["name"]
    #             )

    #         node = cls()
    #         node.id = spec["id"] or node.id
    #         node.title = spec["title"] or node.title
    #         node.description = spec["description"] or node.description
    #         node.properties = spec["properties"] or node.properties
    #         nodes[key] = node

    #     for key in data["nodes"]:
    #         spec = data["nodes"][key]
    #         node = nodes[key]

    #         if isinstance(node, Composite) and "children" in spec:
    #             for cid in spec["children"]:
    #                 node.children.append(nodes[cid])

    #         elif isinstance(node, Decorator) and "child" in spec:
    #             node.child = nodes[spec["child"]]

    #     if data["root"]:
    #         self.root = nodes[data["root"]]

    # def dump(self):
    #     data = {}
    #     custom_names = []

    #     data["title"] = self.title
    #     data["description"] = self.description
    #     data["root"] = self.root.id if self.root else None
    #     data["properties"] = self.properties
    #     data["nodes"] = {}
    #     data["custom_nodes"] = []

    #     if not self.root:
    #         return data

    #     stack = [self.root]
    #     while len(stack) > 0:
    #         node = stack.pop()
    #         spec = {}
    #         spec["id"] = node.id
    #         spec["name"] = node.name
    #         spec["title"] = node.title
    #         spec["description"] = node.description
    #         spec["properties"] = node.properties

    #         name = node.__class__.__name__
    #         if not hasattr(pybehaviorify, name) and name not in custom_names:
    #             subdata = {}
    #             subdata["name"] = name
    #             subdata["title"] = node.title

    #             custom_names.append(name)
    #             data["custom_nodes"].append(subdata)

    #         if isinstance(node, Composite):
    #             children = []
    #             for c in reversed(node.children):
    #                 children.append(c.id)
    #                 stack.append(c)
    #             spec["children"] = children
    #         elif isinstance(node, Decorator):
    #             if node.child:
    #                 stack.append(node.child)
    #                 spec["child"] = node.child.id

    #         data["nodes"][node.id] = spec

    #     return data

    async def tick(self, target: T, blackboard: Blackboard):

        # Create the TICK object
        tick = pybehaviorify.Tick(blackboard=blackboard, tree=self, target=target)

        # Tick node
        if self.root:
            await self.root._execute(tick)

        # Close node from last tick, if needed
        last_open_nodes = blackboard.get("open_nodes", self.id)
        curr_open_nodes = tick._open_nodes

        start = 0
        for node1, node2 in zip(last_open_nodes, curr_open_nodes):
            start += 1
            if node1 != node2:
                break

        # - close nodes
        for i in range(len(last_open_nodes) - 1, start - 1, -1):
            last_open_nodes[i]._close(tick)

        # Populate blackboard
        blackboard.set("open_nodes", curr_open_nodes, self.id)
        blackboard.set("node_count", tick._node_count, self.id)
