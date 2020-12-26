from hst import hostfile, classify

def add_options(parser):
    parser.add_argument('search', metavar='<VALUE>', help='String to search for')
    parser.add_argument('-k', '--key', help='Key to search in', nargs='?')
    parser.set_defaults(func=main)


def main(entries, args):
    return classify.search(entries, args.search, args.key)
