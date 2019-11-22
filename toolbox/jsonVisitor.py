"""Generator for visiting each node in a JSON collections calling a user provided function on each visited node.

Visitor code traverses depth-first but does not use function recursion.  The trade-off is greater memory consumption
over use of stack space.

JSON Specification: https://tools.ietf.org/html/rfc8259
"""
from dataclasses import dataclass
from collections import deque
from typing import List
from itertools import repeat

_JSON_TYPES = {
    # structure
    dict: 'object',
    list: 'array',
    # string
    str: 'string',
    # Literal
    bool: 'boolean',
    type(None): 'null',
    # number
    int: 'number<int>',
    float: 'number<real>',
}


@dataclass(repr=True)
class Node:
    __slots__ = ['name', 'names', 'type', 'value']
    name: str
    names: List[str]
    type: _JSON_TYPES
    value: object


# _____________________________________________________________________________
def __node_type(value):
    return _JSON_TYPES[type(value)]


# _____________________________________________________________________________
def json_visit(data, process_node=lambda x: x):
    aname = '*'
    aname_list = [aname]
    to_visit = deque([Node('', [], __node_type(data), data)])
    while to_visit:
        node = to_visit.popleft()
        yield process_node(node) if process_node else node

        # Process children (if any)
        # if isinstance(node.dataType, dict):
        if type(node.value) is dict:
            children = [Node(n, node.names + [n], __node_type(v), v) for n, v in (dict)(node.value).items()]
            to_visit.extendleft(reversed(children))
        elif type(node.value) is list:
            children = [Node(aname, node.names + aname_list, __node_type(v), v) for v in iter(node.value)]
            to_visit.extendleft(reversed(children))


# _____________________________________________________________________________
def json_visit_org(data, process_node=lambda x: x):
    aname = '*'
    aname_list = [aname]
    to_visit = deque([Node('', [], __node_type(data), data)])
    while True:
        node = to_visit.popleft()
        yield process_node(node) if process_node else node

        # Process children (if any)
        # if isinstance(node.dataType, dict):
        if type(node.value) is dict:
            children = [Node(n, node.names + [n], __node_type(v), v) for n, v in (dict)(node.value).items()]
            to_visit.extendleft(reversed(children))
        elif type(node.value) is list:
            children = [Node(aname, node.names + aname_list, __node_type(v), v) for v in iter(node.value)]
            to_visit.extendleft(reversed(children))
        if not to_visit:
            break
