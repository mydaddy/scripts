# 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144,
# 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946,
# 17711, 28657, 46368, 75025, 121393, 196418, 317811

a, b = 0, 1
print(f'{a}', end = '')
for i in range(12):
    a, b = b, a + b
    print(f', {a}', end = '')

from functools import reduce
fib = lambda n:reduce(lambda x,n:[x[1],x[0]+x[1]], range(n),[0,1])[0]
print()
for i in range(13):
    print(f'{fib(i)}, ', end = '')
