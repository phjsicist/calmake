import argparse
import os

import jinja2

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

latex_jinja_env = jinja2.Environment(
    block_start_string = r'\BLOCK{',
	block_end_string = '}',
	variable_start_string = r'\VAR{',
	variable_end_string = '}',
	comment_start_string = r'\#{',
	comment_end_string = '}',
	line_statement_prefix = r'%%',
	line_comment_prefix = r'%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)

template = latex_jinja_env.get_template('calgrid.tex.jinja')

with open(args.filename, 'w') as f:
    f.write(template.render(month='Mar'))
