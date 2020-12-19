from hst import hostfile

def test_parse_comment_should_extract_existing_timestamp():
    comment = "this is a test comment"
    ts = {
        "2019-02-12": "2019-02-12 00:00:00",
        "2014-05-13 13:12:00": "2014-05-13 13:12:00",
    }
    for timestamp, expected in ts.items():
        res = hostfile.parse_comment(f"[{ timestamp }] # { comment }")
        assert res.get("comment") == comment
        assert res.get("timestamp") == expected

def est_load_file_returns_lines():
    lines = hostfile.load()
    hostfile.write(lines)
    assert False == True
