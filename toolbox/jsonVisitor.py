"""Generator for visiting each node in a JSON collections calling a user provided function on each visited node.

Visitor code traverses depth-first but does not use function recursion.  The trade-off is greater memory consumption
over use of stack space.

JSON Specification: https://tools.ietf.org/html/rfc8259
"""
import typing
from collections import deque
from dataclasses import dataclass

_JSON_TYPES = {
    # string
    str: 'string',
    # number
    int: 'number<int>',
    float: 'number<real>',
    # Literal
    bool: 'boolean',
    type(None): 'null',
    # structure
    dict: 'object',
    list: 'array'
}


@dataclass(slots=True)
class Node:
    name: str
    names: list[str]
    type: _JSON_TYPES
    value: object


# _____________________________________________________________________________
def json_visit(data, process_node=lambda x: x):
    def __node_type(node_value):
        return _JSON_TYPES[type(node_value)]

    array_name = '*'
    array_name_list = [array_name]

    to_visit = deque([Node('', [], __node_type(data), data)])
    while to_visit:
        node = to_visit.popleft()
        yield process_node(node) if process_node else node

        # Process children (if any)
        value = node.value
        if type(value) is dict:
            children = [Node(n, node.names + [n], __node_type(v), v) for n, v in typing.cast(dict, value).items()]
            to_visit.extendleft(reversed(children))
        elif type(value) is list:
            children = [Node(array_name, node.names + array_name_list, __node_type(v), v) for v in
                        typing.cast(list, value)]
            to_visit.extendleft(reversed(children))
