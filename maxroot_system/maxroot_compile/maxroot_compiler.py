# Encode: UTF-8

def compile(filepath) :

    fin = open(filepath, 'rt')

    text = fin.read()
    fin.closed()

    print(text)

    return
