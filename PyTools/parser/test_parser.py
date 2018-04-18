from parser.parser import parse_to_tree


def test_1():
    f_str = "1 + 2"
    parsed = parse_to_tree(f_str)
    desired = {
        'type': 'binary',
        'op': 'add',
        'left': {
            'type': 'const',
            'value': 1
        },
        'right': {
            'type': 'const',
            'value': 2
        }
    }
    assert parsed == desired


def test_2():
    f_str = "sin(-x) + 3"
    parsed = parse_to_tree(f_str)
    desired = {
        'type': 'binary',
        'op': 'add',
        'left': {
            'type': 'func',
            'func': 'sin',
            'args': [
                {
                    'type': 'unary',
                    'op': 'usub',
                    'operand': {
                        'type': 'var',
                        'name': 'x'
                    }
                }
            ]
        },
        'right': {
            'type': 'const',
            'value': 3
        }
    }
    assert parsed == desired
