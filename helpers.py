from collections import namedtuple

# helper functions for use throughout app


def convert_to_named_tuple(result):
    """Given the results of an executed SQL query, return a tuple mapping each column key and value"""
    Record = namedtuple("Record", result.keys())
    return [Record(*r) for r in result.fetchall()]
