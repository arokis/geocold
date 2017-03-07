def open_file(path):
    try:
        with open(path, 'r') as out:
            output = out.read()
        return output
    except IOError:
        print ('[convPY:ERROR] No such File "' + path + '"! Exit!')
        sys.exit(1)

print open_file('plotter.md')