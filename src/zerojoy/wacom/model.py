from typing import NamedTuple, List


class Touch(NamedTuple):
    id: int
    pressed: bool
    x: int
    y: int
    capacitance_x: int
    capacitance_y: int


class TouchRecord(NamedTuple):
    touches: List[Touch]
    event_time: int
    event_time_id: int
