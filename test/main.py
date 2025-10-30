c = float(input())

n = 0
s = 0
while 1 / (2 * n + 1) > c:
    s += ((-1) ** n) * (1 / (2 * n + 1))
    n += 1

s *= 4
print(f"{s:.6f}")