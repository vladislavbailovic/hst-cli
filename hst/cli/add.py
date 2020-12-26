def add_options(parser):
    parser.add_argument('ippos', metavar='<IP>', help='IP to add', nargs='?')
    parser.add_argument('-i', '--ip', help='IP to add', nargs='?')
    parser.add_argument('domainpos', metavar='<DOMAIN>', help='Domain for the IP', nargs='?')
    parser.add_argument('-d', '--domain', help='Domain for the IP', nargs='?')
    parser.set_defaults(func=main)


def main(entries, args):
    print(args)
