def filter(lines, key, value):
    return [ item for item in lines if item.get(key) == value ]

def pluck(lines, what):
    return [ item.get(what) for item in lines ]

def by(lines, what):
    result = {}
    for value in pluck(lines, what):
        result[ value ] = filter(lines, what, value)
    return result

def search(lines, what, key = None):
    result = []
    for entry in lines:
        subject = str(entry) if not key else entry.get(key)
        if what in subject:
            result.append(entry)
    return result
