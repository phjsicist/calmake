import datetime
import os
import subprocess

import jinja2

from .style import CalendarStyle

TEMPLATE_DIR = os.path.dirname(__file__) + os.sep + 'templates'
STYLE_DIR = os.path.dirname(__file__) + os.sep + 'styles'

# define the jinja2 environment for LaTeX
LATEX_JINJA_ENV = jinja2.Environment(
    block_start_string = r'\BLOCK{',
	block_end_string = '}',
	variable_start_string = r'\VAR{',
	variable_end_string = '}',
	comment_start_string = r'\#{',
	comment_end_string = '}',
	line_statement_prefix = r'%%',
	line_comment_prefix = r'%#',
    lstrip_blocks = True,
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath(TEMPLATE_DIR))
)

def calmake(template_name: str|None='default', style_name: str|None=None, year: int|None=None, months: list[int]|None=None, image: str|None=None):
	# set default values for year, months, and image if not provided
	if template_name is None:
		template_name = 'default'
	if year is None:
		year = datetime.datetime.now().year + 1
	if months is None:
		months = list(int(range(1, 13)))
	if image is None:
		image = os.path.abspath('.')

	# load the template
	template_name = template_name.split('.')[0]
	template = LATEX_JINJA_ENV.get_template(template_name + '.tex.jinja')

	# load the base style file
	base_style_path = TEMPLATE_DIR + os.sep + template_name + '.yaml'
	style = CalendarStyle(base_style_path, image, year, months)

	# update the user style if provided
	if style_name is not None:
		if os.path.exists(style_name):
			style_name = os.path.basename(style_name).split('.')[0]
			style_path = os.path.abspath(style_name)
		else:
			style_name = style_name.split('.')[0]
			style_path = STYLE_DIR + os.sep + style_name + '.yaml'
		
		style.deep_update(style_path)
	else:
		style_name = 'default'

	# make output directories
	output_dir = 'output' + os.sep + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '_' + template_name + '_' + style_name
	os.makedirs(output_dir)
	os.makedirs(output_dir + os.sep + 'logs')
	os.makedirs(output_dir + os.sep + 'pdfs')

	# iterate over months and generate calendar sheets
	for month in style.months:
		file_identifier = f'{month:02d}'

		style.update_for_month(month)

		with open(output_dir + os.sep + file_identifier + '.tex', 'w', encoding='utf-8') as f:
			f.write(template.render(**style))

		subprocess.run(['xelatex',
						output_dir + os.sep + file_identifier + '.tex',
						'-output-directory=' + output_dir + os.sep + 'pdfs',
						'-aux-directory=' + output_dir + os.sep + 'logs',
						'-interaction=nonstopmode',
						'-halt-on-error']
		)
