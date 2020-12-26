from hst import hostfile

def add_options(parser):
    parser.add_argument('ippos', metavar='<IP>', help='IP to add', nargs='?')
    parser.add_argument('-i', '--ip', help='IP to add', nargs='?')
    parser.add_argument('domainpos', metavar='<DOMAIN>', help='Domain for the IP', nargs='?')
    parser.add_argument('-d', '--domain', help='Domain for the IP', nargs='?')
    parser.set_defaults(func=main)


def main(entries, args):
    ip = args.ippos or args.ip
    if not ip:
        return entries

    domain = args.domainpos or args.domain
    if not domain:
        return entries

    data = entries[:]
    data.append(
        hostfile.create_entry(ip, domain)
    )
    return data
