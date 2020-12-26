import re
from dateutil.parser import parse as dateparse

from hst import classify

def find(fpath=None):
    return fpath if fpath else "/etc/hosts"

def load(fpath=None):
    with open(find(fpath), "r") as fp:
        rawlines = [line.rstrip() for line in fp.readlines() if line.rstrip()]
    return parse_lines(rawlines)

def parse_lines(rawlines):
    lines = []
    section = "default"
    for line in rawlines:
        if line.lstrip()[0] == "#":
            section = uncomment(line)
            continue
        ip, rest = line.replace(" ", "\t", 1).split("\t", 1)
        lines += parse_line(ip, rest, section)

    return lines

def parse_line(ip, line, section):
    result = line.split("#", 1)
    process = result[0].strip()
    comment = ""
    if len(result) > 1:
        comment = result[1].strip()
    process = process.replace(" ", "\t")

    entries = []
    for entry in process.split("\t"):
        timestamp, note = parse_comment(comment)
        entries.append({
            "ip": ip,
            "domain": entry,
            "timestamp": timestamp,
            "note": note,
            "section": section,
        })
    return entries

def create_entry(ip, domain, timestamp=None, note=None, section=None):
    section = section if section else "default"
    return {
        "ip": ip,
        "domain": domain,
        "timestamp": timestamp,
        "note": note,
        "section": section,
    }

def update_entry(entry, ip=None, domain=None, timestamp=None, note=None, section=None):
    ip = ip if ip else entry.get("ip")
    domain = domain if domain else entry.get("domain")
    timestamp = timestamp if timestamp else entry.get("timestamp")
    note = note if note else entry.get("note")
    section = section if section else entry.get("section")
    return create_entry(ip, domain, timestamp, note, section)

def parse_comment(comment):
    timestamp = ""
    tsstr = ""
    tsre = re.search(r'\[(\d{4}-\d{2}-\d{2}[^\]]*?)\]', comment)
    if tsre:
        tsstr = tsre.group(1)
        timestamp = f"{ dateparse(tsstr) }"
    clean_comment = uncomment(comment.replace(f"[{ tsstr }]", ""))
    return timestamp, clean_comment

def uncomment(line):
    return re.sub(
        r'^\s*#\s*',
        '',
        line
    ).strip()

def format(lines, group_by='section', decorate=True, bare=False):
    content = []
    sections = set(classify.pluck(lines, group_by))
    for section in sections:
        if section and decorate:
            content.append(f"\n# { section }")
        for entry in classify.filter(lines, group_by, section):
            content.append(format_entry(entry, bare))
    return "\n".join(content)

def format_entry(entry, bare=False):
    comment = format_comment(entry)
    if comment:
        comment = f"# { comment }" if not bare else ""
    return f"{ entry.get('ip') }\t{ entry.get('domain') } { comment }".strip()


def format_comment(entry):
    timestamp = entry.get("timestamp")
    if timestamp:
        timestamp = f"[{ timestamp }]"
    comment = entry.get("note", "")
    if timestamp or comment:
        return f"{ timestamp } { comment if comment else '' }".strip()
    return ""
