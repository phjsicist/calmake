import calendar
import datetime
import os
import yaml

from .constants import DAYS1, DAYS2, MONTHS
from .utils import deep_update, extract_exif_rotation

class CalendarStyle(dict):
    def __init__(self, style_path: str, image_path: str, year: int, months: list[int]) -> None:
        with open(style_path, 'r', encoding='utf-8') as f:
            style = yaml.safe_load(f)
        super().__init__(style)

        self.image_path_base = os.path.abspath(image_path)
        self.year = year
        self.months = months

        self._generate_weekdays_line()

    def _generate_weekdays_line(self) -> None:
        weekdays = DAYS2 if self['weekday_long_form'] else DAYS1
        self['weekdays_line'] = self['no_of_weeks_per_line'] * weekdays[self['language']]
        self['no_of_days_per_line'] = 7*self['no_of_weeks_per_line']

    def deep_update(self, style_path: str) -> None:
        """Recursively update the style with another style."""
        with open(style_path, 'r', encoding='utf-8') as f:
            style = yaml.safe_load(f)
        self = deep_update(self, style)

        self._generate_weekdays_line()

    def update_for_month(self, month: int) -> None:
        """Update the style for a specific month."""
        first_weekday = datetime.date(self.year, month, 1).weekday()
        length_of_month = calendar.monthrange(self.year, month)[1]

        self['month_name'] = MONTHS[self['language']][month - 1]
        self['dates'] = [''] * first_weekday + [str(d) for d in range(1, length_of_month + 1)]

        image_name = [n for n in os.listdir(self.image_path_base) if n.startswith(f'{month:02d}')][0]
        image_path = self.image_path_base + os.sep + image_name

        self['image_path'] = image_path.replace('\\', '/')
        self['image_rotation'] = extract_exif_rotation(image_path)
        self['image_caption'] = image_name.split('.')[0].split('_')[1]
