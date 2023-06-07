import time
from math import gcd
import random

time_limit = 5*60  # 5 хвилин

def discrete_logarithm(a, b, n):
    result = 1
    time_limit = 5*60 # 5 хвилин
    start_time = time.time()
    for i in range(n):
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > time_limit:
                return -2
            result = (result * a) % n
            if result == b:
                return i + 1  # Знайдено дискретний логарифм
    return -1  # Дискретний логарифм не знайдено

# Звичайне логарифмування з обеженням 5 хв
# base = 2
# target = 8
# modulus = 13
# result = discrete_logarithm(base, target, modulus)
# if result == -1:
#     print("Дискретний логарифм не знайдено")
# elif result ==-2:
#     print("Time out")
# else:
#     print(f"Дискретний логарифм числа {target} по основі {base} у модулі {modulus} дорівнює {result}")

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
    gcd, x, y = full_gcd(a, mod)
    if gcd == 1:
        return x % mod
    else:
        print("no inverse")
        return 0

def silver_polig_hellman(a, b, n):
    factor_counts = canonical_factorization(n)
    table = {}

    for prime, count in factor_counts.items():
        p = prime
        r_values = []
        for j in range(p):
            power=(n * j) // p
            r = (a**power)%(n+1)
            r_values.append(r)
        table[prime] = r_values

    x_values={}
    
    for prime, r_values in table.items():

        #find x_0
        find_right=(b**(n//prime))%(n+1)
        x_values.setdefault(prime, [])

        if find_right in r_values:
            x_values[prime].append(r_values.index(find_right))


        power=0

        for i in range(factor_counts[prime]):

            power+=(x_values[prime][i]*(prime**(i)))

            find_right = ((b*(inverse(a,n+1)**power))**(n//(prime**(i+2))))%(n+1)

            if find_right in r_values:
                x_values[prime].append(r_values.index(find_right))


    x_sum_value=[]
    for p,x in x_values.items():
        x=0
        for i in range(len(x_values[p])):
            x+=x_values[p][i]*(p**i)
        x_sum_value.append(x)

    mod_values=[]
    for prime, count in factor_counts.items():
        mod_values.append(prime**count)

    if len(x_sum_value) != len(mod_values):
        print("error1")
        return 0
    
    m=len(x_sum_value)
    for i in range(m-1):
        for j in range(i+1,m):
            if gcd(x_sum_value[i], mod_values[j])!=1:
                print("Error2")
                return 0
    x=0
    for i in range(m):
        m_i=mod_values[i]
        n_i=n//m_i
        xi = inverse(n_i, m_i)
        x += x_sum_value[i] * xi * n_i

    x%=n
    return x

# a = int(input("Введіть a: "))
# b = int(input("Введіть b: "))
# n = int(input("Введіть n: "))

def generate_random_numbers():
    a = random.randint(1, 100000)
    b = random.randint(1, 100000)
    n = random.randint(1, 10000000000000000)
    return a, b, n

a=2
b=228
n=383

# a, b, n = generate_random_numbers()

start_time = time.time()
result = silver_polig_hellman(a, b, n)
end_time = time.time()
execution_time = end_time - start_time
print("silver_polig_hellman:")
print("a =", a)
print("b =", b)
print("n =", n)
print("Result:", result)
print("Execution time:", execution_time, "seconds")

    # Тестування функції discrete_logarithm
start_time = time.time()
result = discrete_logarithm(a, b, n)
end_time = time.time()
execution_time = end_time - start_time
print("discrete_logarithm:")
print("a =", a)
print("b =", b)
print("n =", n)
print("Result:", result)
print("Execution time:", execution_time, "seconds")
