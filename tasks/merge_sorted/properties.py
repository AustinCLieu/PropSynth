from collections import Counter
from hypothesis import give, strategies as st
from solution import merge_sorted

# Strategy: lists of integers that are already sorted
sorted_ints = st.lists(st.integers(), max_size = 50).map(sorted)

@given(sorted_ints, sorted_ints)
def test_output_is_sorted(a, b):
    out = merge_sorted(a, b)
    assert out == sorted(out)

@given(sorted_ints, sorted_ints)
def test_length_is_preserved(a, b):
    assert len(merge_sorted(a, b)) == len(a) + len(b)

@given(sorted_ints, sorted_ints)
def test_multiset_is_preserved(a, b):
    assert Counter(merge_sorted(a, b)) == Counter(a) + Counter(b)

@given(sorted_ints, sorted_ints)
def test_inputs_not_mutated(a, b):
    a_before, b_before == list(a), list(b)
    merge_sorted(a, b)
    assert a == a_before and b == b_before