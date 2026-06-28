# Tests if the model's code actually works
# It takes the raw pytest output, parses it, and returns a Verdict (passed or not passed, which property failed, the counterex, and the error)
# It also take's the model's code, sets up a working dir and runs the tests in a docker sandboxm and then hands it off to get a verdict
# Agent loop generates code -> evaluate func runs in sandbox -> parse output func returns verdict -> loop declares success or tries again if not passed

from dataclasses import dataclass # decorator that auto generates boilerplate for making a class




@dataclass
class Verdict:
    passed: bool # passed or not passed the test
    failing_property: str | None # name of specific property that failed 
    # one focused failing property per iteration makes it easier for the model to know what to fix
    counterexample: str | None # smallest input that broke it from Hypothesis
    message: str | None # returns details from pytest showing how the model's code actually failed (ex: assert 2 == 3)
    raw_output: str # full pytest output to keep for tracing
    timed_out: bool = False # defualt value goes after values that aren't default


