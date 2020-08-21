import pytest

from .interface import Dog, Duck


@pytest.fixture
def dog():
    '''Provides a Dog instance'''
    return Dog()


@pytest.fixture
def duck():
    '''Provides a Duck instance'''
    return Duck()
