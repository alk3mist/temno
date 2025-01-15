# Based on https://martinfowler.com/eaaDev/Range.html

"""Functional implementation of the range interface with the exclusive upper bound"""

from collections.abc import Callable, Iterable, Sequence
from itertools import pairwise
from operator import attrgetter
from typing import Protocol, Self, TypeVar

from more_itertools import split_when


class _Comparable(Protocol):
    def __lt__(self, other: Self, /) -> bool: ...


CT = TypeVar("CT", bound=_Comparable)


class ARange(Protocol[CT]):
    start: CT
    end: CT


def sort(ranges: Iterable[ARange[CT]]) -> list[ARange[CT]]:
    return sorted(ranges, key=attrgetter("start"))


def abuts(r: ARange[CT], other: ARange[CT]) -> bool:
    return r.end == other.start


def contiguous(ranges: Iterable[ARange[CT]]) -> bool:
    """Check that ranges are gapless.
    Warning: a sorted sequence required.
    """
    for a, b in pairwise(sort(ranges)):
        if not abuts(a, b):
            return False
    return True


def combination(
    ranges: Sequence[ARange[CT]],
    range_factory: Callable[[CT, CT], ARange[CT]],
) -> ARange[CT]:
    """Combines contiguous ranges into one.
    Warning: a sorted sequence required.
    """
    if not (contiguous(ranges)):
        raise ValueError("Unable to combine ranges")
    return range_factory(ranges[0].start, ranges[-1].end)


def consecutive_groups(ranges: Iterable[ARange[CT]]) -> Iterable[list[ARange[CT]]]:
    """Split ranges when a gap occurs.
    Warning: a sorted sequence required.
    """
    yield from split_when(ranges, lambda a, b: not (abuts(a, b)))


def combine_consecutive_groups(
    ranges: Iterable[ARange[CT]], range_factory: Callable[[CT, CT], ARange[CT]]
) -> Iterable[ARange[CT]]:
    groups = consecutive_groups(sort(ranges))
    combined_ranges = (combination(g, range_factory) for g in groups)
    return combined_ranges
