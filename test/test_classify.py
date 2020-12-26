from hst import classify

def get_host_lines():
    from hst import hostfile
    return hostfile.load()


def test_classification_returns_object():
    res = classify.by(get_host_lines(), "section")
    assert "default" in res.keys()

    res = classify.by(get_host_lines(), "ip")
    assert "127.0.0.1" in res.keys()

def test_search_checks_everything_by_default():
    lines = get_host_lines()
    res1 = classify.search(lines, "localhost")
    assert "localhost" in classify.pluck(res1, "domain")
    res2 = classify.search(lines, "127.0.0.1")
    assert "localhost" in classify.pluck(res2, "domain")

def test_search_checks_key_when_asked():
    lines = get_host_lines()
    res1 = classify.search(lines, "bastion")
    res2 = classify.search(lines, "bastion", "section")
    assert res1 != res2
    assert len(res1) > len(res2)
    assert "bastionmanager" in classify.pluck(res1, "domain")
    assert "bastionmanager" not in classify.pluck(res2, "domain")
