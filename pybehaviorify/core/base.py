from abc import abstractmethod
import enum
from typing import Any, Coroutine
import uuid
from pybehaviorify.core.tick import Tick

BB_IS_OPEN = "is_open"


class NodeStatus(enum.Enum):
    SUCCESS = 1
    FAILURE = 2
    RUNNING = 3
    ERROR = 4


class BaseNode[T]:

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.title: str = self.__class__.__name__
        self.description: str = ""
        self.properties = {}

    @property
    def name(self):
        return self.__class__.__name__

    async def _execute(self, tick: Tick[T]) -> NodeStatus:
        self._enter(tick)

        self._open(tick)

        status = await self._tick(tick)

        if status != NodeStatus.RUNNING:
            self._close(tick)

        self._exit(tick)

        return status

    def _enter(self, tick: Tick[T]):
        tick._enter_node(self)
        self.enter(tick)

    def _open(self, tick: Tick[T]):
        if tick.blackboard.get(BB_IS_OPEN, tick.tree.id, self.id):
            return
        tick._open_node(self)
        tick.blackboard.set(BB_IS_OPEN, True, tick.tree.id, self.id)
        self.open(tick)

    async def _tick(self, tick: Tick[T]):
        tick._tick_node(self)
        return await self.tick(tick)

    def _close(self, tick: Tick[T]):
        if not tick.blackboard.get(BB_IS_OPEN, tick.tree.id, self.id):
            return
        tick._close_node(self)
        tick.blackboard.set(BB_IS_OPEN, False, tick.tree.id, self.id)
        self.close(tick)

    def _exit(self, tick: Tick[T]):
        tick._exit_node(self)
        self.exit(tick)

    def enter(self, tick: Tick[T]):
        pass

    def open(self, tick: Tick[T]):
        pass

    @abstractmethod
    async def tick(self, tick: Tick[T]) -> NodeStatus: ...

    def close(self, tick: Tick[T]):
        pass

    def exit(self, tick: Tick[T]):
        pass
