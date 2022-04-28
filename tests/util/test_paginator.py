from math import ceil
from typing import List, Type

import pytest

from chia.util.paginator import InvalidPageSizeError, InvalidPageSizeLimit, PageOutOfBoundsError, Paginator


@pytest.mark.parametrize("page_size, page_size_limit", [(1, 1), (1, 2), (2, 2), (10, 100), (1000, 1000)])
def test_constructor_valid_inputs(page_size: int, page_size_limit: int) -> None:
    default_paginator: Paginator = Paginator([], page_size, page_size_limit)
    for i in range(1, default_paginator.page_size_limit()):
        paginator: Paginator = Paginator([], i, page_size_limit)
        assert paginator.page_size() == i
        assert paginator.page_count() == 1
        assert paginator.get_page(0) == []


@pytest.mark.parametrize(
    "page_size, page_size_limit, exception",
    [
        (5, -1, InvalidPageSizeLimit),
        (5, 0, InvalidPageSizeLimit),
        (2, 1, InvalidPageSizeError),
        (100, 1, InvalidPageSizeError),
        (1001, 1000, InvalidPageSizeError),
    ],
)
def test_constructor_invalid_inputs(page_size: int, page_size_limit: int, exception: Type[Exception]) -> None:
    with pytest.raises(exception):
        Paginator([], page_size, page_size_limit)


def test_page_count() -> None:
    for page_size in range(1, 10):
        for i in range(0, 10):
            assert Paginator(range(0, i), page_size).page_count() == max(1, ceil(i / page_size))


def test_empty_source() -> None:
    assert Paginator([], 5).get_page(0) == []


@pytest.mark.parametrize(
    "page, expected_data", [(0, [0, 1, 2, 3, 4]), (1, [5, 6, 7, 8, 9]), (2, [10, 11, 12, 13, 14]), (3, [15, 16])]
)
def test_get_page_valid(page: int, expected_data: List[int]) -> None:
    assert Paginator(list(range(0, 17)), 5).get_page(page) == expected_data


@pytest.mark.parametrize("page", [-1000, -10, -1, 5, 10, 1000])
def test_get_page_invalid(page: int) -> None:
    with pytest.raises(PageOutOfBoundsError):
        Paginator(range(0, 17), 5).get_page(page)
