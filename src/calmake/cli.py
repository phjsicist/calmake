import argparse

from .calmake import calmake

def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--template_name', type=str, help='Name of the template file')
    parser.add_argument('-s', '--style_name', type=str, help='Name or path of the style file')
    parser.add_argument('-y', '--year', type=int, help='Year of the calendar, leave empty for next year')
    parser.add_argument('-m', '--months', type=int, action='append', help='Month(s) of the calendar, leave empty for full year')
    parser.add_argument('-i', '--image', type=str, help='Path to folder containing calendar images')
    args = parser.parse_args()

    calmake(**args.__dict__)

if __name__ == '__main__':
    cli()
