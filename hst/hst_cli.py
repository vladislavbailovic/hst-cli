from argparse import ArgumentParser
from hst.cli import add, search
from hst import hostfile, classify


def list_entries(args):
    entries = hostfile.load()
    key = args.group if "group" in args else 'section'
    print(hostfile.format(entries, key))


def add_options(parser):
    parser.add_argument('-g', '--group', help='Group by')
    parser.set_defaults(func=list_entries)


def main():
    parser = ArgumentParser()
    add_options(parser)
    subparsers = parser.add_subparsers()

    add_options(subparsers.add_parser('ls', help='Lists entries'))
    add.add_options(subparsers.add_parser('add', help='Adds new entry'))
    search.add_options(subparsers.add_parser('search', help='Searches entries'))

    options = parser.parse_args()
    options.func(options)


if __name__ == "__main__":
    main()
