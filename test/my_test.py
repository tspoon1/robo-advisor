
# test/my_test.py

from app.robo_advisor import to_usd
from app.robo_advisor import hasNumbers
from app.robo_advisor import couldNotBeFound
from app.robo_advisor import isInvalidTicker


def test_to_usd():
    result = to_usd(5)
    assert result == "$5.00"

def test_hasNumbers():
    result = hasNumbers("testing")
    assert result == False

def test_couldNotBeFound():
    result = couldNotBeFound("xxxxxError Messagexxxxx")
    assert result == True

def test_isInvalidTicker():
    result = isInvalidTicker("1MSFT")
    assert result == True