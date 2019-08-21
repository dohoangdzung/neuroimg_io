def export(filename, content):
    f = open(filename, 'w')
    f.write(content)
    f.close()
