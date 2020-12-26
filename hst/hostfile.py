import re
from dateutil.parser import parse as dateparse
from datetime import datetime

from hst import classify

def find():
    return "test/data/hosts"

def load():
    with open(find(), "r") as fp:
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
        entries.append({
            "ip": ip,
            "domain": entry,
            "data": parse_comment(comment),
            "section": section,
        })
    return entries

def parse_comment(comment):
    timestamp = ""
    tsstr = ""
    tsre = re.search(r'\[(\d{4}-\d{2}-\d{2}[^\]]*?)\]', comment)
    if tsre:
        tsstr = tsre.group(1)
        timestamp = f"{ dateparse(tsstr) }"
    clean_comment = uncomment(comment.replace(f"[{ tsstr }]", ""))
    return {
        "timestamp": timestamp,
        "comment": clean_comment
    }

def uncomment(line):
    return re.sub(
        r'^\s*#\s*',
        '',
        line
    ).strip()

def format(lines):
    content = []
    sections = set(classify.pluck(lines, "section"))
    for section in sections:
        content.append(f"\n# { section }")
        for entry in classify.filter(lines, "section", section):
            comment = parse_data(entry.get("data"))
            if comment:
                comment = f"# { comment }"
            content.append(
                f"{ entry.get('ip') }\t{ entry.get('domain') } { comment }"
            )
    return "\n".join(content)

def parse_data(data):
    timestamp = data.get("timestamp")
    if timestamp:
        timestamp = f"[{ timestamp }]"
    return f"{ timestamp } { data.get('comment') }".strip()
