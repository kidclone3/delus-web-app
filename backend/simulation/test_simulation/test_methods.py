import sys

import pytest
import os

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(SCRIPT_DIR))
print(SCRIPT_DIR)
from simulation.methods import *

def test_nxn_matrix():
    grid_count = 3
    obstacles_set = {'0:0', '1:1', '2:2'}

    expected = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0]
    ]
    print(os.getcwd())
    assert build_graph(obstacles_set, grid_count) == expected

    grid_count2 = 6
    obstacles_set2 = {'0:2', '0:3', '1:2', '1:3', '5:5', '4:5'}
    expected2 = [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0],
    ];
    assert build_graph(obstacles_set2, grid_count2) == expected2