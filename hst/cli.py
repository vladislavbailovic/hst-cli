from hst import hostfile, classify

def main():
    entries = hostfile.load()
    nondefault = classify.without(entries, 'section', "default")
    print(hostfile.format(nondefault))

if __name__ == "__main__":
    main()
