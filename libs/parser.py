import ast
from ast2json import ast2json
from argparse import ArgumentParser, RawTextHelpFormatter

def parseToTree(function):
    def purify(json):
        t = json['_type']
        if t == 'BinOp':
            return purifyBinaryOp(json)
        elif t =='UnaryOp':
            return purifyUnaryOp(json)
        elif t == 'Call':
            return purifyCall(json)
        elif t == 'Num':
            return purifyNum(json)
        elif t == 'Name':
            return purifyName(json)
        else:
            raise Exception('Unrecognized Type {}'.format(t))

    def purifyBinaryOp(json):
        jsonNew = {
            'type': 'binary',
            'op': json['op']['_type'].lower(),
            'left': purify(json['left']),
            'right': purify(json['right'])}
        return jsonNew

    def purifyUnaryOp(json):
        jsonNew = {
            'type': 'unary',
            'op': json['op']['_type'].lower(),
            'operand': purify(json['operand'])
        }
        return jsonNew

    def purifyCall(json):
        jsonNew = {
            'type': 'func',
            'func': json['func']['id'],
            'args': list(map(purify, json['args']))
        }
        return jsonNew

    def purifyNum(json):
        jsonNew = {
            'type': 'const',
            'value': json['n']
        }
        return jsonNew

    def purifyName(json):
        jsonNew = {
            'type': 'var',
            'name': json['id']
        }
        return jsonNew

    json = ast2json(ast.parse(function, mode = 'eval'))['body']
    return purify(json)


def main(args):
    mode = args.mode
    if mode == 'parse':
        result = parseToTree("".join(args.function))
    print(result)

parser = ArgumentParser(description="Calculus Api",
                        formatter_class=RawTextHelpFormatter)

parser.add_argument("--mode",
                    type=str,
                    help='Api mode')

parser.add_argument("--function",
                    type=str,
                    nargs="+",
                    help='Function to be parsed')

args = parser.parse_args()

main(args)
