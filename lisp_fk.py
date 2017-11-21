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

parser = ox.make_parser([
    	('sexpr : OPEN CLOSE', lambda x,y: '()'),
    	('sexpr : OPEN expr CLOSE', lambda x,y,z: y),
    	('expr : atom expr', lambda x,y: (x,) + y),
    	('expr : atom', lambda x: (x,)),
    	('atom : sexpr', lambda x: x),
    	('atom : NUMBER', lambda x: x),
    	('atom : SYMBOL', lambda x: x),
], tokens)


@click.command()
@click.argument('source', type=click.File('r'))
def make_ast(source):
	source_code = source.read()
	tokens = lexer(source_code)
	print(tokens)
	ast = parser(tokens)
	pprint.pprint(ast)

if __name__ == '__main__':
	make_ast()
