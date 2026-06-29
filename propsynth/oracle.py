# Tests if the model's code actually works
# It takes the raw pytest output, parses it, and returns a Verdict (passed or not passed, which property failed, the counterex, and the error)
# It also take's the model's code, sets up a working dir and runs the tests in a docker sandboxm and then hands it off to get a verdict
# Agent loop generates code -> evaluate func runs in sandbox -> parse output func returns verdict -> loop declares success or tries again if not passed

from dataclasses import dataclass # decorator that auto generates boilerplate for making a class
import re # Python's regex module. We use it to extract text form pytest's output



# Output class from the oracle. This is the format of what returns after a piece of code is ran in the sandbox and judged by the oracle
@dataclass
class Verdict:
    passed: bool # passed or not passed the test
    failing_property: str | None # name of specific property that failed 
    # one focused failing property per iteration makes it easier for the model to know what to fix
    counterexample: str | None # smallest input that broke it from Hypothesis
    message: str | None # returns details from pytest showing how the model's code actually failed (ex: assert 2 == 3)
    raw_output: str # full pytest output to keep for tracing
    timed_out: bool = False # defualt value goes after values that aren't default

# Regex parsing patterns
# re.compile takes a pattern string and pre-builds it into a reuable pattern object for efficiency
# r"..." allows for single "\""
# _, leading underscore, is a python convention meaning that something is internal to the module, not meant to be used from the outside

# finds pytest's failure summary line, ex pytest ouput: FAILED properties.py::test_length_preserved - ...
# FAILED = FAILED, \s+ matches one or more spaces, \S+ matches one or more non-space chars, :: matches ::, (\S+) matches test name and captures it
_FAILED_RE = re.compile(r"FAILED\s+\S+::(\S+)") 


# finds the counterexample
# ex pytest output: 
# Falsifying example: test_length_preserved(
# a=[0], b=[0],
# )
# Falsifying example: = Falsifying example:, \s* is 0 or more whitespace, (.*?) captures any characters but the ? makes it non greedy so it stops at the first place the next pattern can match
# (?:\n\n|\nE\s|\n_{3,}|\Z) is the non-capturing group, ?: means "group these together but don't capture this part as output"
# \n\n is a blank line (two newlines in a row) as counterex block is usually followed by a blank line
# \nE\s is a new line followed by E (start of an error deatil line)
# \n_{3,} is a newline followed by 3 or more underscores
# \Z is the very end of the string
# normally . matches any char except newlines, re.DOTALL lets . match newlines too
_FALSIFYING_RE = re.compile(r"Falsifying example:\s*(.*?)(?:\n\n|\nE\s|\n_{3,}|\Z)", re.DOTALL)


# finds pytest's error detail lines
# ex: E   assert 1 == 2
# ^ means start of a line
# E matches E
# \s+ matches one or more spaces
# (.*) captures everything else on the line, 0 or more of any chars
# $ means end of line so (.*) only goes to the end of the line
# normaly, ^ and $ match only the very start and very end of the entire text. re.MULTILINE means that ^ and $ match the start and end of each line in the text
_ERROR_LINE_RE = re.compile(r"^E\s+(.*)$", re.MULTILINE)

# Takes raw pytest output, parses through it using the regex patterns, and returns a Verdict
def parse_pytest_output(raw_output: str, returncode: int, timed_out: bool = False) -> Verdict:
    if timed_out: # code timed out
        return Verdict(False, None, None, "Execution timed out", raw_output, True)
    if returncode == 0: # passed with no issues
        return Verdict(True, None, None, None, raw_output)
    
    failed = _FAILED_RE.search(raw_output)
    failing_property = failed.group(1) if failed else None

    falsifying = _FALSIFYING_RE.search(raw_output)
    counterexample = falsifying.group(1).strip if falsifying else None

    errors = _ERROR_LINE_RE.findall(raw_output) # Can have multiple E error lines
    message = " ".join(e.strip() for e in errors).strip() or None

    return Verdict(False, failing_property, counterexample, message, raw_output)


    