import time
import random
from Server import Server

def H(s, x):
    res = ''
    x += str(s)
    for i in range(len(x)):
        a = (ord(x[(i+1) % len(x)]) + ord(x[(i-1) % len(x)])) % (i+1)#(ord(x[i]) + i)
        res += str(a)
    return res

if __name__ == '__main__':
    print('Регистрация')
    server = Server()
    ts = int(time.time()) % 10000
    N = 0xEEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3
    g = 2
    I = input('Введите логин:')
    p = input('Введите пароль:')
    x = int(H(ts, p))
    v = g ** x % N
    server.add(I,v,ts)
    print("Регистрация завершена")
    while True:
        print('Авторизация')
        email = input('Введите логин:')
        password = input('Введите пароль:')
        emails = list(map(lambda x: x[0], server.database))
        if email not in emails:
            print('Неверный логин или пароль')
            break
        a = random.randint(10, 100)
        A = g ** a % N
        verificator = server.database[emails.index(email)][1]
        salt = server.database[emails.index(email)][2]
        b = random.randint(10, 100)
        B = 3 * verificator + g ^ b % N
        u = int(H(A, str(B)))
        if u == 0:
            print('Соединение разорвано')
            break
        x = int(H(salt, password))
        S1 = ((B - 3 * (g ^ x % N)) ^ (a + u * x)) % N
        K1 = H('', str(S1))
        S2 = ((A * (v ^ u % N)) ^ b) % N
        K2 = H('', str(S2))
        print(K1 == K2)