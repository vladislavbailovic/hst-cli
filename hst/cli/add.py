from dateutil.parser import parse as dateparse
import datetime

from hst import hostfile

def add_options(parser):
    parser.add_argument('ippos', metavar='<IP>', help='IP to add', nargs='?')
    parser.add_argument('-i', '--ip', help='IP to add', nargs='?')
    parser.add_argument('domainpos', metavar='<DOMAIN>', help='Domain for the IP', nargs='?')
    parser.add_argument('-d', '--domain', help='Domain for the IP', nargs='?')
    parser.add_argument('-t', '--timestamp', help='Overrride timestamp - dash for none', nargs='?')
    parser.set_defaults(func=main)


def main(entries, args):
    ip = args.ippos or args.ip
    if not ip:
        return entries

    domain = args.domainpos or args.domain
    if not domain:
        return entries

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if args.timestamp:
        timestamp = "" if args.timestamp == "-" else dateparse(args.timestamp)

    data = entries[:]
    data.append(
        hostfile.create_entry(ip, domain, timestamp)
    )
    return data
