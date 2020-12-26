from argparse import ArgumentParser
import os
from hst.cli import add, search
from hst import hostfile, classify


def list_entries(entries, args):
    return entries


def add_options(parser):
    parser.add_argument('-f', '--file', help='Input file')
    parser.add_argument('-g', '--group', help='Group by', default='section')
    parser.add_argument('-n', '--no-decorate', help='Do not decorate', action='store_true')
    parser.add_argument('-b', '--bare', help='Strip comments', action='store_true')
    parser.set_defaults(func=list_entries)


def main():
    parser = ArgumentParser()
    add_options(parser)
    subparsers = parser.add_subparsers()

    add_options(subparsers.add_parser('ls', help='Lists entries'))
    add.add_options(subparsers.add_parser('add', help='Adds new entry'))
    search.add_options(subparsers.add_parser('search', help='Searches entries'))

    options = parser.parse_args()
    entries = hostfile.load(options.file)
    print(hostfile.format(
        options.func(entries, options),
        options.group,
        not options.no_decorate,
        options.bare
    ))


if __name__ == "__main__":
    main()
