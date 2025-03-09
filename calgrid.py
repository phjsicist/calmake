import argparse
import calendar
import datetime
import os

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
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)

language = 'fr'

tex_kwargs = {
	'month': 2,
    'year': 2024,
	'weekdays_line': ' & '.join(DAYS2[language]) + '\\\\',
    'dates_grid': '1 & 2 & 3 & 4 & 5 & 6 & 7 \\\\ 8 & 9 & 10 & 11 & 12 & 13 & 14 \\\\ 15 & 16 & 17 & 18 & 19 & 20 & 21 \\\\ 22 & 23 & 24 & 25 & 26 & 27 & 28 \\\\ 29 & 30 & 31 & & & &',
}

first_weekday = datetime.date(tex_kwargs['year'], tex_kwargs['month'], 1).weekday()
length_of_month = calendar.monthrange(tex_kwargs['year'], tex_kwargs['month'])[1]
dates_list = [''] * first_weekday + [str(d) for d in range(1, length_of_month + 1)]

tex_kwargs['dates_grid'] = ''
for i in range(0, len(dates_list), 7):
	tex_kwargs['dates_grid'] += ' & '.join(dates_list[i:i+7]) + ' \\\\ '

tex_kwargs['month_name'] = MONTHS[language][tex_kwargs['month'] - 1]

template = latex_jinja_env.get_template('calgrid.tex.jinja')

with open(args.filename, 'w', encoding='utf-8') as f:
    f.write(template.render(**tex_kwargs))
