import sys
import pytest
import src.generator as gen  # The file ../src/generator.py

"""
This file (test_estimator.py) contains the unit tests for the minvime/estimator.py file.
"""

def test_min_max_baseline():
    temp = gen.generate_min_max_baseline(10,100)
    assert len(temp) == 9000
    assert min(temp) >= 10
    assert max(temp) <= 100

