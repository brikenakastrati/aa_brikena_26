
T = 'JIM SAW ME IN A BARBERSHOP'
P = 'BARBER'


# 1. Brute Force
def brute_force(T, P):
    n, m = len(T), len(P)

    for i in range(n - m + 1):
        j = 0

        while j < m and P[j] == T[i + j]:
            j += 1

        if j == m:
            return i

    return -1


# 2. Shift Table
def shift_table(P):
    m = len(P)
    table = {}

    for j in range(m - 1):
        table[P[j]] = m - 1 - j

    return table


# Helps calculate the shift distance
def shift(table, c, m):
    return table[c] if c in table else m


# 3. Horspool
def horspool(T, P):
    n, m = len(T), len(P)
    table = shift_table(P)
    i = m - 1

    while i <= n - 1:
        print("Horspool alignment:", i - m + 1)

        k = 0
        while k <= m - 1 and P[m - 1 - k] == T[i - k]:
            k += 1

        if k == m:
            return i - m + 1

        i += shift(table, T[i], m)

    return -1


# 4. Horspool 2
def horspool2(T, P):
    n, m = len(T), len(P)
    table = shift_table(P)
    i = m - 1

    while i <= n - 1:
        k = 0
        while k <= m - 1 and P[m - 1 - k] == T[i - k]:
            k += 1

        if k == m:
            return i - m + 1

        i += shift(table, T[i - k], m)

    return -1


# Results
print("shift_table:", shift_table(P))
print("brute_force:", brute_force(T, P))
print("horspool:", horspool(T, P))
print("horspool2:", horspool2(T, P))
