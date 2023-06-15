import time
from math import gcd
import random

time_limit = 5*60  # 5 хвилин


def discrete_logarithm(a, b, n):
    result = 1
    time_limit = 5*60  # 5 хвилин
    start_time = time.time()
    x=1
    for i in range(1,n):
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > time_limit:
            return -2
        x*=a
        x=x%n
        if(x==b):
            return i
    return -1  # Неможливо знайти дискретний логарифм



# Звичайне логарифмування з обеженням 5 хв
# a = 1920
# b = 1746
# p = 2473
# result = discrete_logarithm(a, b, p)
# if result == -1:
#     print("Дискретний логарифм не знайдено")
# elif result ==-2:
#     print("Time out")
# else:
#     print(f"Дискретний логарифм числа {a} по основі {b} у модулі {p} дорівнює {result}")

def canonical_factorization(n):
    factors = []
    factor_counts = {}

    divisor = 2
    while divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            n = n // divisor
            if divisor in factor_counts:
                factor_counts[divisor] += 1
            else:
                factor_counts[divisor] = 1
        else:
            divisor += 1

    return factor_counts

def full_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x_prev, y_prev = full_gcd(b, a % b)
    x = y_prev
    y = x_prev - (a // b) * y_prev
    return gcd, x, y

def inverse(a, mod):
    mod+=1
    gcd, x, y = full_gcd(a, mod)
    if gcd != 1:
        print("no inverse")
        return 0
    a_1 = x % mod
    #print(str(a) + "^-1 mod " + str(mod) + " = " + str(a_1))
    return a_1

#x = x0 + x1pi + . . . + xl−1p
def calc_x_value(a_inv, b, n, p, table_row, X, k):
    for i in range(len(X)):
        b = (b * pow(a_inv, X[i] * pow(p, i, n), n)) % n
    b = pow(b, n // (p ** (k + 1)), n)
    for i in range(len(table_row)):
        if b == table_row[i]:
            return i

def solve_sys_congr(x_values, mod):
    x = 0
    M = []
    i = 0
    for a, m in x_values:
        mi = mod // m
        gcd, u, v = full_gcd(mi, m)
        if gcd != 1:
            print("no inverse")
            return 0
        mi_inv = u % m
        x = (x + a * mi * mi_inv) % mod
        M.append((mi, mi_inv))
        i += 1
    return x

def silver_polig_hellman(a, b, n):
    n-=1
    factor_counts = canonical_factorization(n)
    #print(factor_counts)
    table = {}

    for prime, count in factor_counts.items():
        p = prime
        r_values = []
        for j in range(p):
            power=(n * j) // p
            r = (a**power)%(n+1)
            r_values.append(r)
        table[prime] = r_values

    #print(table)

#шукаємо х для подальшого розв'язку системи  (х та pl)
    x_values = []
    a_inv=inverse(a,n)
    for p in factor_counts:
        X = []
        x = 0
        l = factor_counts[p]
        pl = p ** l
        for i in range(l):
            xi = calc_x_value(a_inv, b, n+1, p, table[p], X, i)
            X.append(xi)
            x = (x + xi * p ** i) % pl
        x_values.append((x, pl))
    x = solve_sys_congr(x_values, n )
    return x

# a = int(input("Введіть a: "))
# b = int(input("Введіть b: "))
# n = int(input("Введіть n: "))

a = 691
b = 4757
n = 34583

start_time = time.time()
result = silver_polig_hellman(a, b, n)
end_time = time.time()
execution_time = end_time - start_time
print("silver_polig_hellman:")
print("a =", a)
print("b =", b)
print("n =", n)
print("Result:", result)
print("time:", execution_time, "s")

    # Тестування функції discrete_logarithm
start_time = time.time()
result = discrete_logarithm(a, b, n)
end_time = time.time()
execution_time = end_time - start_time
print("discrete_log3arithm:")
print("a =", a)
print("b =", b)
print("n =", n)
print("Result:", result)
print("time:", execution_time, "s")
