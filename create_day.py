#!/usr/bin/env python
import sys

from jinja2 import Environment, FileSystemLoader

def main():
    year = int(sys.argv[1])
    day = int(sys.argv[2])

    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.py.jinja2")

    with open(f"{year}/{day:02}.py", "w") as f:
        f.write(template.render(day=f'{day:02}'))

    open(f"{year}/inputs/{day:02}.txt", "w").close()
    open(f"{year}/inputs/{day:02}_test.txt", "w").close()


if __name__ == '__main__':
    main()
