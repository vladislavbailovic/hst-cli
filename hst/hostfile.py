import re
from dateutil.parser import parse as dateparse
from datetime import datetime

def find():
    return "hosts"

def load():
    with open(find(), "r") as fp:
        rawlines = [line.rstrip() for line in fp.readlines() if line.rstrip()]
    lines = {}
    for line in rawlines:
        if line.lstrip()[0] == "#":
            continue # comment line
        ip, rest = line.replace(" ", "\t", 1).split("\t", 1)
        lines[ ip ] = parse_line(rest, lines.get(ip, []))

    return lines

def parse_line(line, previous=[]):
    result = line.split("#", 1)
    process = result[0].strip()
    comment = ""
    if len(result) > 1:
        comment = result[1].strip()

    entries = []
    for entry in process.split("\t"):
        entries.append({
            "domain": entry,
            "data": parse_comment(comment),
        })
    return previous + entries

def parse_comment(comment):
    tsre = re.search(r'\[(\d{4}-\d{2}-\d{2}[^\]]*?)\]', comment)
    if not tsre:
        return { "timestamp": "", "comment": comment }
    tsstr = tsre.group(1)
    timestamp = f"{ dateparse(tsstr) }"
    clean_comment = comment.replace(f"[{ tsstr }]", "").strip()
    clean_comment = clean_comment.replace("#", "", 1).strip()
    return {
        "timestamp": timestamp,
        "comment": clean_comment
    }

def write(lines):
    content = []
    for ip, entries in lines.items():
        for entry in entries:
            content.append(
                f"{ ip }\t{ entry.get('domain') } # { parse_data(entry.get('data')) }"
            )
    print("\n".join(content))

def parse_data(data):
    timestamp = data.get("timestamp")
    if not timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    return f"[{ timestamp }] { data.get('data') }"
