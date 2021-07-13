import sys


def comparison(first_string, second_string):
    if '*' not in second_string:
        if len(first_string) != len(second_string):
            return False
        else:
            for j in range(len(second_string)):
                if first_string[j] != second_string[j]:
                    return False
    else:
        substring = ''
        for j in range(len(second_string)):
            if second_string[j] == '*':
                continue
            else:
                substring = substring + second_string[j]
                x = j + 1
                if x < len(second_string) and second_string[x] != '*':
                    continue
            if substring not in first_string:
                return False
            else:
                substring = ''
    return True


if __name__ == '__main__':
    first_string = sys.argv[1]
    second_string = sys.argv[2]

    if comparison(first_string, second_string):
        print('OK')
    else:
        print('KO')
