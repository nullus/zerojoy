from abc import abstractmethod, ABC, ABCMeta
from typing import Tuple, List


class RangeSet(ABC, metaclass=ABCMeta):

    @abstractmethod
    def __contains__(self, item: int) -> bool:
        pass

    @abstractmethod
    def insert(self, item: int) -> 'RangeSet':
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @property
    @abstractmethod
    def _range(self) -> range:
        pass

    @abstractmethod
    def ranges(self) -> List[Tuple[int, int]]:
        pass

    @abstractmethod
    def _depth(self) -> int:
        pass


class Empty(RangeSet):

    def __contains__(self, item: int) -> bool:
        return False

    def insert(self, item: int) -> RangeSet:
        return Node(item, item + 1)

    def is_empty(self) -> bool:
        return True

    @property
    def _range(self) -> range:
        raise AttributeError("undefined range")

    def ranges(self) -> List[Tuple[int, int]]:
        raise AttributeError("undefined range")

    def _depth(self) -> int:
        raise AttributeError("undefined depth")

    def __repr__(self) -> str:
        return "Empty()"


class Span(RangeSet):

    def __init__(self, left: RangeSet, right: RangeSet) -> None:
        super().__init__()
        self._left = left
        self._right = right

    def __contains__(self, item: int) -> bool:
        if item < self._mid:
            return item in self._range and item in self._left
        else:
            return item in self._range and item in self._right

    def insert(self, item: int) -> 'RangeSet':
        if item < self._mid:
            return Span(self._left.insert(item), self._right).__balance()
        else:
            return Span(self._left, self._right.insert(item)).__balance()

    def is_empty(self) -> bool:
        return False

    @property
    def _range(self) -> range:
        return range(self._left._range.start, self._right._range.stop)

    @property
    def _mid(self) -> int:
        return (self._left._range.stop + self._right._range.start) // 2

    def ranges(self) -> List[Tuple[int, int]]:
        left = self._left.ranges()
        right = self._right.ranges()
        if left[-1][1] >= right[0][0]:
            # If the mid tuple overlaps, merge it
            return left[:-1] + [(left[-1][0], right[0][1])] + right[1:]
        else:
            return left + right

    def _depth(self) -> int:
        return max(self._left._depth(), self._right._depth()) + 1

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._left)}, {repr(self._right)})"

    def __left_rotate(self) -> RangeSet:
        if isinstance(self._right, Span):
            return Span(Span(self._left, self._right._left), self._right._right)
        else:
            # No rotation is possible
            return self

    def __right_rotate(self) -> RangeSet:
        if isinstance(self._left, Span):
            return Span(self._left._left, Span(self._left._right, self._right))
        else:
            # No rotation is possible
            return self

    def __balance(self) -> RangeSet:
        if self._left._depth() > self._right._depth() * 2:
            return self.__right_rotate()
        elif self._right._depth() > self._left._depth() * 2:
            return self.__left_rotate()
        else:
            return self


class Node(RangeSet):

    def __init__(self, from_: int, to: int) -> None:
        super().__init__()
        self._from = from_
        self._to = to

    def __contains__(self, item: int) -> bool:
        return item in self._range

    def insert(self, item: int) -> RangeSet:
        if item in self:
            return self
        elif item == self._from - 1:
            return Node(self._from - 1, self._to)
        elif item == self._to:
            return Node(self._from, self._to + 1)
        elif item < self._from - 1:
            return Span(Empty().insert(item), self)
        elif item > self._to:
            return Span(self, Empty().insert(item))

    def is_empty(self) -> bool:
        return False

    @property
    def _range(self) -> range:
        return range(self._from, self._to)

    def ranges(self) -> List[Tuple[int, int]]:
        return [(self._from, self._to)]

    def _depth(self) -> int:
        return 1

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._from)}, {repr(self._to)})"
