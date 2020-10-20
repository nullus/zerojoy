from zerojoy.collections import *


def test_empty_range_set_is_empty():
    assert Empty().is_empty() is True


def test_empty_range_set_contains_nothing():
    empty = Empty()
    assert 1 not in empty
    assert 3 not in empty
    assert 4 not in empty


def test_empty_range_set_insert_contains_item():
    empty = Empty()
    n = empty.insert(5)
    assert 5 in n


def test_range_set_node_is_not_empty():
    node = Node(5, 6)
    assert node.is_empty() is False


def test_range_set_node_insert_adjacent():
    node = Node(5, 6)
    left = node.insert(4)
    right = node.insert(6)
    assert 4 in left
    assert 6 in right
    assert 5 in left and 5 in right


def test_range_set_node_insert_distant():
    node = Node(5, 6)
    left = node.insert(1)
    right = node.insert(10)
    assert 1 in left and 5 in left
    assert 10 in right and 5 in right
    assert 3 not in left and 7 not in right


def test_range_set_span_insert_distant():
    range_set = Span(Node(1, 2), Node(5, 7))
    left = range_set.insert(-5)
    right = range_set.insert(10)
    assert -5 in left and 1 in left and 6 in left
    assert 1 in right and 6 in right and 10 in right
    assert -3 not in left and 8 not in right


def test_range_set_span_is_not_empty():
    range_set = Span(Node(1, 2), Node(5, 7))
    assert range_set.is_empty() is False


def test_range_set_ranges():
    range_set = Span(Span(Node(-10, -5), Node(1, 4)), Span(Node(5, 7), Node(10, 13)))
    assert [(-10, -5), (1, 4), (5, 7), (10, 13)] == range_set.ranges()


def test_range_set_node_zero_depth():
    range_set = Node(3, 4)
    assert 1 == range_set._depth()


def test_range_set_span_depth_of_tallest_branch():
    range_set = Span(Node(1, 2), Span(Node(2, 3), Span(Node(3, 4), Node(4, 5))))
    assert 4 == range_set._depth()


def test_range_set_ranges_should_merge_adjacent_ranges():
    range_set = Span(Node(0, 5), Span(Node(5, 10), Node(10, 20)))
    assert [(0, 20)] == range_set.ranges()
