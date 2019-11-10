import json
import logging

from toolbox import jsonVisitor as jv

logger = logging.getLogger(__name__)


# _____________________________________________________________________________
def json_node_name(node):
    return node.name


# _____________________________________________________________________________
def json_node_names(node):
    return '.'.join(map(str, node.names))


# _____________________________________________________________________________
def test_json_types():
    with open(r'.\data\data-types.json') as f:
        data = json.load(f)
    lst = list(jv.json_visit(data))
    assert lst[0] == jv.Node('', [], 'object', {'_object': {}, '_array': [], '_string': '',
        '_bool.true': True, '_bool.false': False, '_int': 0, '_number': 0.0, '_null': None})
    assert lst[1] == jv.Node('_object', ['_object'], 'object', {})
    assert lst[2] == jv.Node('_array', ['_array'], 'array', [])
    assert lst[3] == jv.Node('_string', ['_string'], 'string', '')
    assert lst[4] == jv.Node('_bool.true', ['_bool.true'], 'boolean', True)
    assert lst[5] == jv.Node('_bool.false', ['_bool.false'], 'boolean', False)
    assert lst[6] == jv.Node('_int', ['_int'], 'number<int>', 0)
    assert lst[7] == jv.Node('_number', ['_number'], 'number<real>', 0.0)
    assert lst[8] == jv.Node('_null', ['_null'], 'null', None)


# _____________________________________________________________________________
def test_json_arrays():
    with open(r'.\data\data-arrays.json') as f:
        data = json.load(f)
    lst = list(jv.json_visit(data, json_node_names))
    assert lst == ['', '*', '*.*', '*.*._a1-1', '*.*._a1-2',
        '*.*._a1-2._a1-2-1', '*.*._a1-2._a1-2-2', '*.*._a1-2._a1-2-3',
        '*.*._a1-3',
        '*', '*.*', '*.*._a2-1', '*.*._a2-2',
        '*.*._a2-2._a2-2-1', '*.*._a2-2._a2-2-2', '*.*._a2-2._a2-2-3', '*.*._a2-3',
        '*',  '*.*', '*.*._a3-1', '*.*._a3-2', '*.*._a3-3']


# _____________________________________________________________________________
def test_json_names():
    with open(r'.\data\data-books.json') as f:
        data = json.load(f)
    lst = sorted(set(jv.json_visit(data, json_node_names)))
    assert lst == ['', 'catalogue', 'catalogue.*', 'catalogue.*.author', 'catalogue.*.format', 'catalogue.*.isbn10',
                'catalogue.*.isbn13', 'catalogue.*.publicationDate', 'catalogue.*.title']
