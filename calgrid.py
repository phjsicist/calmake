import argparse
import calendar
import collections.abc
import datetime
import os
import subprocess

import jinja2
import yaml

from constants import DAYS1, DAYS2, MONTHS

def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--template-name', type=str, help='Name of the template file', default='default.tex.jinja')
parser.add_argument('-c', '--config', type=str, help='Name or path of the config file')
parser.add_argument('-y', '--year', type=int, help='Year of the calendar', default=datetime.datetime.now().year)
parser.add_argument('-m', '--month', type=int, help='Month(s) of the calendar, leave empty for full year', action='append')
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
    lstrip_blocks = True,
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('.\\templates'))
)

template_name = args.template_name.split('.')[0]
template_path = os.path.abspath('templates' + os.sep + template_name + '.tex.jinja')
template = latex_jinja_env.get_template(template_name + '.tex.jinja')

base_config_path = os.path.abspath('templates' + os.sep + template_name + '.yaml')
with open(base_config_path, 'r', encoding='utf-8') as f:
	config = yaml.safe_load(f)

if args.config:
	if os.path.exists(args.config):
		config_name = os.path.basename(args.config).split('.')[0]
		config_path = os.path.abspath(args.config)
	else:
		config_name = args.config.split('.')[0]
		config_path = os.path.abspath('templates' + os.sep + config_name + '.yaml')
    
	with open(config_path, 'r', encoding='utf-8') as f:
		update(config, yaml.safe_load(f))
else:
	config_name = 'default'

config['year'] = args.year
config['weekdays_line'] = config['no_of_weeks_per_line'] * DAYS1[config['language']]

output_dir = 'output' + os.sep + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '_' + template_name + '_' + config_name
os.makedirs(output_dir)
os.makedirs(output_dir + os.sep + 'logs')
os.makedirs(output_dir + os.sep + 'pdfs')

months = args.month if args.month else [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
for month in months:
	file_identifier = f'{month:02d}'

	first_weekday = datetime.date(config['year'], month, 1).weekday()
	length_of_month = calendar.monthrange(config['year'], month)[1]

	config['month_name'] = MONTHS[config['language']][month - 1]
	config['dates'] = [''] * first_weekday + [str(d) for d in range(1, length_of_month + 1)]

	with open(output_dir + os.sep + file_identifier + '.tex', 'w', encoding='utf-8') as f:
		f.write(template.render(**config))

	subprocess.run(['xelatex',
					output_dir + os.sep + file_identifier + '.tex',
					'-output-directory=' + output_dir + os.sep + 'pdfs',
					'-aux-directory=' + output_dir + os.sep + 'logs',
					'-interaction=nonstopmode',
					'-halt-on-error']
	)
