import ast
from ast2json import ast2json


def parse_to_tree(f_str):

    def purify(json):
        t = json['_type']
        if t == 'BinOp':
            return purify_binary_op(json)
        elif t =='UnaryOp':
            return purify_unary_op(json)
        elif t == 'Call':
            return purify_call(json)
        elif t == 'Num':
            return purify_num(json)
        elif t == 'Name':
            return purify_name(json)
        else:
            raise Exception('Unrecognized Type {}'.format(t))

    def purify_binary_op(json):
        json_new = {
            'type': 'binary',
            'op': json['op']['_type'].lower(),
            'left': purify(json['left']),
            'right': purify(json['right'])}
        return json_new

    def purify_unary_op(json):
        json_new = {
            'type': 'unary',
            'op': json['op']['_type'].lower(),
            'operand': purify(json['operand'])
        }
        return json_new

    def purify_call(json):
        json_new = {
            'type': 'func',
            'func': json['func']['id'],
            'args': list(map(purify, json['args']))
        }
        return json_new

    def purify_num(json):
        json_new = {
            'type': 'const',
            'value': json['n']
        }
        return json_new

    def purify_name(json):
        json_new = {
            'type': 'var',
            'name': json['id']
        }
        return json_new

    json = ast2json(ast.parse(f_str, mode='eval'))['body']
    return purify(json)
