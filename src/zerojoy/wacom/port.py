from logging import getLogger
from typing import Tuple, NamedTuple, List, Optional

from zerojoy.wacom.model import TouchRecord, Touch


class Region(NamedTuple):
    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def min_x(self):
        return min(self.x1, self.x2)

    @property
    def max_x(self):
        return max(self.x1, self.x2)

    @property
    def min_y(self):
        return min(self.y1, self.y2)

    @property
    def max_y(self):
        return max(self.y1, self.y2)

    def __contains__(self, point: Tuple[int, int]):
        return self.min_x <= point[0] <= self.max_x and self.min_y <= point[1] <= self.max_y


def grid_region(left: int, top: int, width: int, height: int) -> Region:
    """
    Basic grid layout based on 12mm buttons with 8mm spacing.

    This gives us 11 x 7 button layout
    """

    wacom_resolution = 40  # points/mm
    button_size = 16
    button_spacing = 4

    # Margin to centre button layout
    margin_x = 160
    margin_y = 240

    def dimension_to_points(n: int) -> int:
        return (n * button_size + (n - 1) * button_spacing) * wacom_resolution - 1

    def offset_to_points(n: int) -> int:
        return n * (button_size + button_spacing) * wacom_resolution

    x = offset_to_points(left) + margin_x
    y = offset_to_points(top) + margin_y
    return Region(
        x, y,
        x + dimension_to_points(width), y + dimension_to_points(height)
    )


class Button(NamedTuple):
    id: int
    pressed: bool


class Axes(NamedTuple):
    id: int
    x: int
    y: int


class Axis(NamedTuple):
    id: int
    u: int


class Hat(NamedTuple):
    id: int
    r: int


class TouchRegionControl:
    pass


class TouchRegionButton(TouchRegionControl):
    def __init__(self, region: Region, id_: int) -> None:
        super().__init__()
        self.region = region
        self.id = id_

    def map(self, touches: List[Touch]) -> Button:
        return Button(self.id, any((t.x, t.y) in self.region for t in touches if t.pressed))


class TouchRegionAxes(TouchRegionControl):
    def __init__(self, region: Region, id_: int, min_: int, max_: int) -> None:
        super().__init__()
        self._last_touch_id = None
        self.id = id_
        self.center = (min_ + max_) // 2
        self.min = min_
        self.max = max_
        self.region = region

    @staticmethod
    def normalise(x: int, from0: int, from1: int, to0: int, to1: int) -> int:
        """
        Normalise x from range from0 - from1 to to0 - to1 avoiding loss of precision. Clamp initial value
        """

        return (max(min(x, max(from0, from1)), min(from0, from1)) - from0) * (to1 - to0) // (from1 - from0) + to0

    def map(self, touches: List[Touch]) -> Axes:
        touch = next((t for t in touches if ((t.x, t.y) in self.region or t.id == self._last_touch_id) and t.pressed), None)
        if touch:
            # Find first matching touch in region, or matching continuously seen ID
            self._last_touch_id = touch.id
            return Axes(self.id,
                        self.normalise(touch.x, self.region.x1, self.region.x2, self.min, self.max),
                        self.normalise(touch.y, self.region.y1, self.region.y2, self.min, self.max))
        else:
            # Otherwise center
            self._last_touch_id = None
            return Axes(self.id, self.center, self.center)


class TouchRegionAxisX(TouchRegionControl):
    def __init__(self, region: Region, id_: int, min_: int, max_: int) -> None:
        super().__init__()
        self._last_touch_id = None
        self.id = id_
        self.center = (min_ + max_) // 2
        self.min = min_
        self.max = max_
        self.region = region

    @staticmethod
    def normalise(x: int, from0: int, from1: int, to0: int, to1: int) -> int:
        """
        Normalise x from range from0 - from1 to to0 - to1 avoiding loss of precision. Clamp initial value
        """

        return (max(min(x, max(from0, from1)), min(from0, from1)) - from0) * (to1 - to0) // (from1 - from0) + to0

    def map(self, touches: List[Touch]) -> Axis:
        touch = next((t for t in touches if ((t.x, t.y) in self.region or t.id == self._last_touch_id) and t.pressed), None)
        if touch:
            # Find first matching touch in region, or matching continuously seen ID
            self._last_touch_id = touch.id
            return Axis(self.id,
                        self.normalise(touch.x, self.region.x1, self.region.x2, self.min, self.max))
        else:
            # Otherwise center
            self._last_touch_id = None
            return Axis(self.id, self.center)


class TouchRegionSliderY(TouchRegionControl):
    def __init__(self, region: Region, id_: int, min_: int, max_: int) -> None:
        super().__init__()
        self.id = id_
        self.min = min_
        self.max = max_
        self.region = region
        self._last_value = Axis(self.id, self.min)

    @staticmethod
    def normalise(x: int, from0: int, from1: int, to0: int, to1: int) -> int:
        """
        Normalise x from range from0 - from1 to to0 - to1 avoiding loss of precision. Clamp initial value
        """

        return (max(min(x, max(from0, from1)), min(from0, from1)) - from0) * (to1 - to0) // (from1 - from0) + to0

    def map(self, touches: List[Touch]) -> Axis:
        touch = next((t for t in touches if (t.x, t.y) in self.region and t.pressed), None)
        if touch:
            # Find first matching touch in region, or matching continuously seen ID
            self._last_value = Axis(self.id,
                                    self.normalise(touch.y, self.region.y1, self.region.y2, self.min, self.max))
        return self._last_value


class TouchRegionHat(TouchRegionControl):
    def __init__(self, region: Region, id_: int) -> None:
        super().__init__()
        self.id = id_
        self.region = region

    @staticmethod
    def normalise(x: int, from0: int, from1: int, to0: int, to1: int) -> int:
        """
        Normalise x from range from0 - from1 to to0 - to1 avoiding loss of precision. Clamp initial value
        """

        return (max(min(x, max(from0, from1)), min(from0, from1)) - from0) * (to1 - to0) // (from1 - from0) + to0

    def map(self, touches: List[Touch]) -> Hat:
        touch = next((t for t in touches if (t.x, t.y) in self.region and t.pressed), None)
        if touch:
            # Find first matching touch in region, or matching continuously seen ID
            address = self.normalise(touch.y, self.region.y1, self.region.y2 - 1, 0, 3) * 3 + self.normalise(touch.x, self.region.x1, self.region.x2 - 1, 0, 3)
            return Hat(self.id, [8, 1, 2, 7, 0, 3, 6, 5, 4, 0, 0, 0, 0][address])

        else:
            return Hat(self.id, 0)


class TouchMapper:
    def __init__(self, handlers) -> None:
        super().__init__()
        self.log = getLogger(__name__)

        def much_button(left: int, top: int, width: int, height: int, start_numbering: int) -> List[TouchRegionControl]:
            return [
                TouchRegionButton(grid_region(left + x, top + y, 1, 1), start_numbering + (y * width + x))
                for x in range(0, width)
                for y in range(0, height)
            ]

        self.mappings: List[TouchRegionControl] = much_button(1, 3, 4, 3, 1) + much_button(6, 4, 2, 2, 13) + [
            TouchRegionAxisX(grid_region(0, 6, 11, 1), 25, 0, 255),
            TouchRegionSliderY(grid_region(5, 0, 1, 6), 26, 0, 255),
            TouchRegionHat(grid_region(8, 4, 2, 2), 27),
        ]
        self._handlers = handlers

    def submit(self, record: TouchRecord):
        outputs = [
            m.map(record.touches) for m in self.mappings
        ]
        self.log.debug("%s.submit(): mapped outputs: %s", self.__class__.__name__, outputs)
        for handler in self._handlers:
            handler.submit(outputs)

