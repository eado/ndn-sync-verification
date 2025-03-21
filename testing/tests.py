def convert(text):
    out = ''
    for char in text:
        if char.isnumeric():
            out += char
    return out


out = open('tests.all', 'w')
for i in range(1, 6):
    start = ''
    probe = ''
    for line in open(f'../tests/tests{i}.txt'):
        c = convert(line)
        if len(c) != 0:
            if 'State Vector' in line:
                start = c
            elif 'Recv' in line:
                probe = c
                if start == '':
                    print('another went wrong')
                out.write(f'{start} {probe}\n')
                start = ''
                probe = ''

            else:
                print("something went wrong " + c)

out.close()
