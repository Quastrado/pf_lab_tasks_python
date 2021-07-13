import sys


def num_to_base(num, base):
    i = 0
    rep = {}
    for symb in base:
        rep[str(i)] = symb
        i += 1
    new_num_string=''
    current=num
    while current!=0:
        remainder=current%len(rep)
        if 36>remainder>9:
            remainder_string=rep[remainder]
        elif remainder>=36:
            remainder_string='('+str(remainder)+')'
        else:
            remainder_string=str(remainder)
        new_num_string=remainder_string+new_num_string
        current=current//len(rep)
    return new_num_string


def main(argv):
    num = abs(int(sys.argv[1]))    
    base = sys.argv[2]
    symbols = '0123456789abcdefghijklmnopqrstuvwxyz'
    if base.startswith('0') and base in symbols:
        return num_to_base(num, base)
    else:
        sys.stdout.write('Система счисления может содержать числовые символы и буквы латинского алфавита.В последовательности от нуля до символа "z"\n')
        sys.exit()


if __name__ == '__main__':
   result = main(sys.argv)
   print(result)
