"""Generator for visiting each node in a JSON collections calling a user provided function on each visited node.

Visitor code traverses depth-first but does not use function recursion.  The trade-off is greater memory consumption
over use of stack space.

JSON Specification: https://tools.ietf.org/html/rfc8259
"""
from collections import deque
from dataclasses import dataclass
from typing import List, Dict

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


@dataclass
class Node:
    __slots__ = ['name', 'names', 'type', 'value']
    name: str
    names: list[str]
    type: _JSON_TYPES
    value: object


# _____________________________________________________________________________
def json_visit(data, process_node=lambda x: x):
    def __node_type(value):
        return _JSON_TYPES[type(value)]

    array_name = '*'
    array_name_list = [array_name]

    to_visit = deque([Node('', [], __node_type(data), data)])
    while to_visit:
        node = to_visit.popleft()
        yield process_node(node) if process_node else node

        # Process children (if any)
        value = node.value
        if type(value) is Dict:
            children = [Node(n, node.names + [n], __node_type(v), v) for n, v in value.items()]
            to_visit.extendleft(reversed(children))
        elif type(value) is List:
            children = [Node(array_name, node.names + array_name_list, __node_type(v), v) for v in value]
            to_visit.extendleft(reversed(children))
