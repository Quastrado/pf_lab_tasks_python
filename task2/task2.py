import re
import sys

from math import sqrt


def jsonfy(s:str)->object:
    obj = eval(s, type('js', (dict,), dict(__getitem__=lambda s, n: n))())
    return obj


def coordinates_calculation(t, A, B):
    x = A[0] + (B[0] - A[0]) * t
    y = A[1] + (B[1] - A[1]) * t
    z = A[2] + (B[2] - A[2]) * t
    return [x, y, z]


def print_result(result):
    for value in result:
        print(value)


if __name__ == '__main__':
    src = sys.argv[1]

    with open(src, 'r') as f:
        data = f.read()
        line = re.search(r'\{\[.*\]+\}', data)[0]
        line = line.replace('{', '[').replace('}', ']')
        data = re.sub(r'\{\[.*\]+\}', line, data)

    data = jsonfy(data)

    A = (data['line'][0][0], data['line'][0][1], data['line'][0][2])
    B = (data['line'][1][0], data['line'][1][1], data['line'][1][2])
    C = (data['sphere']['center'][0], data['sphere']['center'][1], data['sphere']['center'][2])
    R = data['sphere']['radius']

    a = (B[0] - A[0])**2 + (B[1] - A[1])**2 + (B[2] - A[2])**2
    b = -2 * ((B[0] - A[0])*(C[0] - A[0]) + (B[1] - A[1])*(C[1] - A[1]) + (B[2] - A[2])*(C[2] - A[2]))
    c = (C[0] - A[0])**2 + (C[1] - A[1])**2 + (C[2] - A[2])**2 - R**2

    discr = b**2 - 4*a*c
    if discr > 0:
        t1 = -b + sqrt(discr) / (2 * a)
        t2 = -b - sqrt(discr) / (2 * a)
        print_result(coordinates_calculation(t1, A, B))
        print('')
        print_result(coordinates_calculation(t2, A, B))
    elif discr == 0:
        t = -b / (2 * a)
        print_result(coordinates_calculation(t, A, B))
    else:
        print('Коллизий не найдено')
