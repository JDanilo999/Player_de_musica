
from random import randint
from time import sleep
print('como você está?')
v = int(input('digite \033[1;30;41m(1)\033[m para: estou bem, digite \033[1;34;40m(2)\033[m para: não estou bem'))
print('\033[1;33;40mcarregando...\033[m')
sleep(3)

if v == 1:
    print('\033[4;32mque bom que você está bem')
else:
    print('que pena')


