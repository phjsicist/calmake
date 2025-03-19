import argparse
import calendar
import datetime
import os
import subprocess

import jinja2

from constants import DAYS1, DAYS2, MONTHS

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
    lstrip_blocks = True,
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('.\\templates'))
)

language = 'de'
no_of_weeks_per_line = 1
month = 3
year = 2025

first_weekday = datetime.date(year, month, 1).weekday()
length_of_month = calendar.monthrange(year, month)[1]

tex_kwargs = {
	'month': month,
    'year': year,
    'no_of_weeks_per_line': no_of_weeks_per_line,
	'weekdays_line': no_of_weeks_per_line * DAYS1[language],
    'month_name': MONTHS[language][month - 1],
	'dates': [''] * first_weekday + [str(d) for d in range(1, length_of_month + 1)],
}

template = latex_jinja_env.get_template('calgrid.tex.jinja')

output_dir = 'output' + os.sep + args.filename
os.makedirs(output_dir, exist_ok=True)

with open(output_dir + os.sep + args.filename + '.tex', 'w', encoding='utf-8') as f:
    f.write(template.render(**tex_kwargs))

subprocess.run(['pdflatex',
                output_dir + os.sep + args.filename + '.tex',
                '-output-directory=' + output_dir,
                '-interaction=nonstopmode']
)
