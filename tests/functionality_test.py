"""This file should be placed along with the executable file."""

import pytest
from main import *


@pytest.mark.parametrize('arr1, arr2, expected', 
                    [ 
                        ([1, 2, 3, 4], [2, 4], [1, 3]),
                        ([1, 2, 3, 4], [], [1, 2, 3, 4]),
                        ([], [], []),
                        ([1, 2, 3, 4], [1, 2, 3, 4], []),
                    ])
def test_check_values(arr1, arr2, expected):
    assert check(arr1, arr2) == expected
    
@pytest.mark.parametrize('arr1, arr2, expected', 
                    [ 
                        ([1, 2, 3, 4], [5], ValueError),
                        ([1, 2, 3, 4], [1, 5], ValueError),
                        ([], [2], ValueError),
                    ])
def test_check_raises(arr1, arr2, expected):
    try:
        check(arr1, arr2)
    except expected:
        assert 1
    else:
        assert 0
