from typing import NamedTuple, List


class Touch(NamedTuple):
    id: int
    down: bool
    x: int
    y: int
    capacitance: int


class TouchRecord(NamedTuple):
    touches: List[Touch]
    sequence: int