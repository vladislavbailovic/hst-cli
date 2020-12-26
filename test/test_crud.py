import re
from hst import hostfile, classify

def test_added_entry_with_no_extra_data_does_not_add_comment():
    entries = hostfile.load("test/data/hosts")
    entry = hostfile.create_entry( 'xx.xx.xx.xx', "test.test" )
    entries.append(entry)
    out = hostfile.format(entries)
    assert None != re.search(r"^xx.xx.xx.xx\stest.test$", out, re.MULTILINE)


def test_added_entry_with_timestamp_adds_comment():
    entries = hostfile.load("test/data/hosts")
    entry = hostfile.create_entry( 'xx.xx.xx.xx', "test.test", { "timestamp": "2020-12-12" } )
    entries.append(entry)
    out = hostfile.format(entries)
    assert None != re.search(r"^xx.xx.xx.xx\stest.test # \[2020-12-12\]$", out, re.MULTILINE)


def test_update_entries():
    entries = hostfile.load("test/data/hosts")
    changed = [
        hostfile.update_entry(entry, 'xx.xx.xx.xx') \
        if entry.get("domain") == "bastionmanager" else entry
        for entry in entries
    ]
    original_lines = [
        hostfile.format_entry(entry)
        for entry in classify.filter(entries, 'domain', "bastionmanager")
    ]
    changed_lines = [
        hostfile.format_entry(entry)
        for entry in classify.filter(changed, 'domain', "bastionmanager")
    ]
    assert len(original_lines) > 0
    assert len(changed_lines) > 0
    assert len(original_lines) == len(changed_lines)

def test_remove_section():
    entries = hostfile.load("test/data/hosts")
    nondefault = classify.without(entries, 'section', "default")
    assert "default" not in classify.pluck(nondefault, 'section')
