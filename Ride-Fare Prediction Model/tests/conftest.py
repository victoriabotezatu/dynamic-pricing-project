import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pricing  


@pytest.fixture(scope="session")
def data():
    """The raw dataset, loaded once per test session."""
    return pricing.load_data()


@pytest.fixture(scope="session")
def split(data):
    """A single fixed (train_df, test_df) split shared by every test."""
    return pricing.split_data(data, seed=pricing.SEED)


@pytest.fixture(scope="session")
def train_df(split):
    return split[0]


@pytest.fixture(scope="session")
def test_df(split):
    return split[1]
