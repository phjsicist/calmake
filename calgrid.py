import argparse
import datetime
import os
import subprocess

import jinja2

from config import CalendarConfig

# define command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--template-name', type=str, help='Name of the template file', default='default.tex.jinja')
parser.add_argument('-c', '--config', type=str, help='Name or path of the config file')
parser.add_argument('-y', '--year', type=int, help='Year of the calendar', default=datetime.datetime.now().year+1)
parser.add_argument('-m', '--month', type=int, help='Month(s) of the calendar, leave empty for full year', action='append')
parser.add_argument('-i', '--image', type=str, help='Path to folder containing calendar images')
args = parser.parse_args()

# define the jinja2 environment for LaTeX
latex_jinja_env = jinja2.Environment(
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
	loader = jinja2.FileSystemLoader(os.path.abspath('.\\templates'))
)

# load the template
template_name = args.template_name.split('.')[0]
template_path = os.path.abspath('templates' + os.sep + template_name + '.tex.jinja')
template = latex_jinja_env.get_template(template_name + '.tex.jinja')

# load the base config file
base_config_path = os.path.abspath('templates' + os.sep + template_name + '.yaml')
config = CalendarConfig(base_config_path, args.image, args.year, args.month)

# update the user config if provided
if args.config:
	if os.path.exists(args.config):
		config_name = os.path.basename(args.config).split('.')[0]
		config_path = os.path.abspath(args.config)
	else:
		config_name = args.config.split('.')[0]
		config_path = os.path.abspath('configs' + os.sep + config_name + '.yaml')
    
	config.deep_update(config_path)
else:
	config_name = 'default'

# make output directories
output_dir = 'output' + os.sep + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '_' + template_name + '_' + config_name
os.makedirs(output_dir)
os.makedirs(output_dir + os.sep + 'logs')
os.makedirs(output_dir + os.sep + 'pdfs')

# iterate over months and generate calendar sheets
for month in config.months:
	file_identifier = f'{month:02d}'

	config.update_for_month(month)

	with open(output_dir + os.sep + file_identifier + '.tex', 'w', encoding='utf-8') as f:
		f.write(template.render(**config))

	subprocess.run(['xelatex',
					output_dir + os.sep + file_identifier + '.tex',
					'-output-directory=' + output_dir + os.sep + 'pdfs',
					'-aux-directory=' + output_dir + os.sep + 'logs',
					'-interaction=nonstopmode',
					'-halt-on-error']
	)
