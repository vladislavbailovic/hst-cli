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

        res = hostfile.parse_comment(f"[{ timestamp }] { comment }")
        assert res.get("comment") == comment
        assert res.get("timestamp") == expected

def test_parse_comment_should_leave_timestamp_empty_if_theres_none():
    res = hostfile.parse_comment(f"# this is a comment")
    assert "this is a comment" == res["comment"]
    assert "" == res["timestamp"]

def test_uncomment_strips_leading_hash_only():
    tests = [
        "this is a test comment",
        "this # is a test comment",
        "this # is # a # test comment",
    ]
    for expected in tests:
       res = hostfile.uncomment(f"# { expected }")
       assert res == expected

def test_parse_lines_should_separate_space_separated_domains():
    tests = {
        "00.000.000.00 amherst.edu wordpress.amherst.edu": 2,
        "00.000.000.00 amherst.edu": 1,
    }
    for line, expected in tests.items():
        domains = hostfile.parse_lines([line])
        assert expected == len(domains)
