from typing import Any, Dict, Optional
import copy


class Blackboard:
    def __init__(self):
        self.__base_memory = {}
        self.__tree_memory = {}

    def __get_tree_memory(self, tree_scope):
        if tree_scope not in self.__tree_memory:
            self.__tree_memory[tree_scope] = {"node_memory": {}, "open_nodes": []}

        return self.__tree_memory[tree_scope]

    def __get_node_memory(self, tree_memory, node_scope):
        memory = tree_memory["node_memory"]

        if node_scope not in memory:
            memory[node_scope] = {}

        return memory[node_scope]

    def __get_memory(self, tree_scope, node_scope):
        memory = self.__base_memory

        if tree_scope is not None:
            memory = self.__get_tree_memory(tree_scope)

            if node_scope is not None:
                memory = self.__get_node_memory(memory, node_scope)

        return memory

    def dump(self):
        return {
            "base": copy.deepcopy(self.__base_memory),
            "tree": copy.deepcopy(self.__tree_memory),
        }

    def load(self, dump: Dict):
        self.__base_memory = copy.deepcopy(dump["base"])
        self.__tree_memory = copy.deepcopy(dump["tree"])

    def set(
        self,
        key: str,
        value: Any,
        tree_scope: Optional[str] = None,
        node_scope: Optional[str] = None,
    ):
        memory = self.__get_memory(tree_scope, node_scope)
        memory[key] = value

    def get(
        self,
        key: str,
        tree_scope: Optional[str] = None,
        node_scope: Optional[str] = None,
    ) -> Any:
        memory = self.__get_memory(tree_scope, node_scope)
        return memory.get(key)
