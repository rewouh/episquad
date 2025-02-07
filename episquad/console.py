def log(m):
    print(m)

def logf(b, m, v):
    if not b:
        print(f'An error occured: {m}')
    else:
        print(m)

    return b, v

def listit(l):
    return f'[ {', '.join([f'*{e}*' for e in l])} ]'
