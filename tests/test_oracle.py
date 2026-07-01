# unit tests for pytest parser to cover success, failure, and timed out case 

from propsynth.oracle import parse_pytest_output 

# pytest's convention is that any function named test_ is a test. Don't call them yourself. Pytest sees the test function and assert statements
# assert <condition> passes silently if the condition is true, fails the test if it's false

# success case
def test_parse_succes():
    v = parse_pytest_output("4 passed in 0.53s", 0) # fake pytest success string and a success return code of 0
    assert v.passed # parse_pytest_output should have set passed = True because returncode is 0
    assert v.failing_property is None # failing_property should also have been set by the function to None

# tests the parser handles a real failure completely, updating the Verdict correctly
def test_parse_failure_extracts_everything():
    raw = """
    ...multi-line fake pytest output...
    """ # multi-line triple-quoted string, what pytest may print on failure
    v = parse_pytest_output(raw, 1) # fake failrue output and return code 1 should skip timeout and success branches in parse_pytest_output
    assert not v.passed # passes if v.passed is false
    assert v.failing_property == "test_length_preserved" # tests that parser, _FAILED_RE regex, pulled exact property name from FAILED...:test_length_preserved line
    assert "a=[0]" in v.counterexample # tests _FALSIFYING_RE regex
    assert "1 == 2" in v.message # tests _ERROR_LINE_RE regex

# Checks the timedout path
def test_parse_timeout():
    v = parse_pytest_output("", -1, timed_out = True) # calls parser with empty output, return code -1, and timed_out = True
    assert not v.passed # time out should have a not passed verdict
    assert v.timed_out # verdict should say timed out is true
