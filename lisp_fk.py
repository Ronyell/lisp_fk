import ox
import click
import pprint

lexer = ox.make_lexer([
	('OPEN', r'\('),
	('CLOSE', r'\)'),
	('SYMBOL', r'[-a-zA-Z]+'),
	('NUMBER', r'[0-9]+'),
	('ignore_COMMENT', r';[^\n]*'),
	('ignore_NEWLINE', r'\s+'),
])


tokens = ['SYMBOL',
      	'NUMBER',
      	'OPEN',
      	'CLOSE']

operator = lambda type_op: ('operator', type_op)
op = lambda op: (op)

parser = ox.make_parser([
    	('sexpr : OPEN expr CLOSE', lambda x,y,z: y),
    	('expr : atom expr', lambda x,y: (x,) + y),
    	('expr : atom', lambda x: (x,)),
    	('atom : sexpr', op),
    	('atom : NUMBER', op),
    	('atom : SYMBOL', op),
], tokens)


@click.command()
@click.argument('source', type=click.File('r'))
def make_tree(source):
	program = source.read()
	tokens = lexer(program)

	tree = parser(tokens)
	pprint.pprint(tree)

if __name__ == '__main__':
	make_tree()
