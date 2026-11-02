
class _Deleted:
    def __repr__(self):
        return "DELETED"  # so it prints nicely when we print a table


DELETED = _Deleted()


# ===========================================================================
# TASK 1 - functions from the lecture
# ===========================================================================

# Turns a key into a number.
# A number is used as it is; a word becomes the sum of its letters'
# positions in the alphabet (A = 1, B = 2, ... Z = 26).
def num(key):
    if isinstance(key, (int, float)):
        return key
    s = 0
    for c in key:
        s += ord(c) - 64  # ord('A') is 65, so 'A' -> 1
    return s


# The hash function: the key's number mod the table size m.
# The result is always a valid index from 0 to m - 1.
def h(key, m):
    return num(key) % m


# Open hashing (separate chaining).
# Every cell holds a list; each key is appended to the list at its hash.
def chainedTable(keys, m):
    table = []
    for _ in range(m):
        table.append([])            # one empty list per cell
    for k in keys:
        table[h(k, m)].append(k)    # new key goes to the end of its list
    return table


# Closed hashing with linear probing - insert.
# Start at the key's hash; if the cell is taken, try the next one,
# wrapping around from the last cell to cell 0.
def probeInsert(table, key):
    m = len(table)
    i = h(key, m)
    while table[i] is not None:     # cell taken -> move to the next one
        i = (i + 1) % m
    table[i] = key                  # first empty cell found
    return i


# Linear probing - find.
# Walks the same path as probeInsert. Stops at the first empty cell,
# because the key would have been placed there if it existed.
def probeFind(table, key):
    m = len(table)
    i = h(key, m)
    while table[i] is not None:
        if table[i] == key:
            return i                # found: return its index
        i = (i + 1) % m
    return -1                       # reached an empty cell: not in the table


# Linear probing - remove (lecture version).
# Same as probeFind, but the found cell is emptied (set to None).
# Problem: this can break the path for keys stored after it.
def probeRemove(table, key):
    m = len(table)
    i = h(key, m)
    while table[i] is not None:
        if table[i] == key:
            table[i] = None         # empty the cell
            return i
        i = (i + 1) % m
    return -1


# ===========================================================================
# TASK 2 - new functions
# ===========================================================================

# Lazy deletion: like probeRemove, but writes DELETED instead of None.
# DELETED is not None, so probeFind keeps walking past it and can still
# find keys that sit behind the removed one.
def remove(table, key):
    m = len(table)
    i = h(key, m)
    while table[i] is not None:     # only cells on the key's probe path
        if table[i] == key:
            table[i] = DELETED      # mark as removed instead of emptying
            return i
        i = (i + 1) % m
    return -1                       # key not in the table


# Double hashing - insert.
# Start at h(key, m) like linear probing, but jump by a step s that comes
# from a second hash. Different keys get different steps, which avoids
# long runs of taken cells. A DELETED cell is not empty, so we walk past it.
def doubleHashInsert(table, key):
    m = len(table)
    i = h(key, m)
    s = m - 2 - num(key) % (m - 2)  # second hash, computed once per key
    while table[i] is not None:
        i = (i + s) % m             # jump by s, wrapping around
    table[i] = key
    return i


# Double hashing - find.
# Follows exactly the same path as doubleHashInsert.
# Returns the index when the cell holds the key, -1 at an empty cell.
def doubleHashFind(table, key):
    m = len(table)
    i = h(key, m)
    s = m - 2 - num(key) % (m - 2)  # same step as when the key was inserted
    while table[i] is not None:     # DELETED cells are walked past
        if table[i] == key:
            return i
        i = (i + s) % m
    return -1


# The largest number of key comparisons in a successful search,
# for each of the three methods. Returns {chained, linear, double}.
# keys is only read, never changed (the keys are distinct and fewer than m).
def maxComparisons(keys, m):
    # 1. Build three tables of size m from the same keys
    chained = chainedTable(keys, m)
    linear = [None] * m
    double = [None] * m
    for k in keys:
        probeInsert(linear, k)
        doubleHashInsert(double, k)

    # 2. chained: a search may compare against every key in one list,
    #    so the worst case is the length of the longest list
    worst_chained = max(len(lst) for lst in chained)

    # 3. linear and double: for each key, walk its path from h(key, m)
    #    and count the cells up to and including its own cell
    worst_linear = 0
    worst_double = 0
    for k in keys:
        # linear probing: step of 1
        i = h(k, m)
        count = 1                       # the first cell we look at
        while linear[i] != k:
            i = (i + 1) % m
            count += 1
        worst_linear = max(worst_linear, count)

        # double hashing: step s from the second hash
        i = h(k, m)
        s = m - 2 - num(k) % (m - 2)
        count = 1
        while double[i] != k:
            i = (i + s) % m
            count += 1
        worst_double = max(worst_double, count)

    return {"chained": worst_chained, "linear": worst_linear,
            "double": worst_double}


# True if n is a prime number (trial division up to the square root).
def isPrime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


# The smallest prime >= n.
def nextPrime(n):
    while not isPrime(n):
        n += 1
    return n


# Insert that keeps the load factor alpha = n / m at 0.5 or below.
# Returns the same table if it did not grow, the new one if it did.
def insertGrow(table, key):
    m = len(table)

    # 1. Count the keys n in the table. None and DELETED are not keys.
    n = sum(1 for x in table if x is not None and x is not DELETED)

    # 2. If adding one more key would make alpha > 0.5, grow:
    #    new size = smallest prime >= 2m, and the old keys are inserted
    #    again with probeInsert, from cell 0 to the end.
    #    DELETED cells are skipped, so the new table has none.
    if (n + 1) / m > 0.5:
        new_table = [None] * nextPrime(2 * m)
        for x in table:
            if x is not None and x is not DELETED:
                probeInsert(new_table, x)   # rehash into the new size
        table = new_table

    # 3. Insert the key and return the table
    probeInsert(table, key)
    return table


# ===========================================================================
# Checks - only run when the file is started directly (python hashing.py)
# ===========================================================================
if __name__ == "__main__":
    # The lecture's example words
    W = ['A', 'FOOL', 'AND', 'HIS', 'MONEY',
         'ARE', 'SOON', 'PARTED']

    # Task 1 trace - run in this order
    T = [None] * 13
    for w in W:
        probeInsert(T, w)

    print("chainedTable(W, 13)[11] ->", chainedTable(W, 13)[11])
    print("probeFind(T, 'PARTED')  ->", probeFind(T, 'PARTED'))
    print("probeFind(T, 'KID')     ->", probeFind(T, 'KID'))
    print("probeRemove(T, 'ARE')   ->", probeRemove(T, 'ARE'))
    print("probeFind(T, 'SOON')    ->", probeFind(T, 'SOON'))

    # Task 2 - remove, with the table built again (expected: 11, 12, -1, -1)
    T = [None] * 13
    for w in W:
        probeInsert(T, w)

    print()
    print("remove(T, 'ARE')        ->", remove(T, 'ARE'))
    print("probeFind(T, 'SOON')    ->", probeFind(T, 'SOON'))
    print("probeFind(T, 'ARE')     ->", probeFind(T, 'ARE'))
    print("remove(T, 'KID')        ->", remove(T, 'KID'))

    # Task 2 - double hashing, the lecture's numbers
    # Expected D: [None, 56, None, 31, 75, 19, None, None, 30, 20, None]
    N = [30, 20, 56, 75, 31, 19]
    D = [None] * 11                 # table size 11 is prime
    for k in N:
        doubleHashInsert(D, k)

    print()
    print("D                       ->", D)
    print("doubleHashFind(D, 19)   ->", doubleHashFind(D, 19))
    print("doubleHashFind(D, 42)   ->", doubleHashFind(D, 42))

    # Task 2 - maxComparisons
    # Expected: {chained: 3, linear: 6, double: 2}
    #           {chained: 2, linear: 2, double: 3}
    print()
    print("maxComparisons(N, 11)   ->", maxComparisons(N, 11))
    print("maxComparisons(W, 13)   ->", maxComparisons(W, 13))

    # Task 2 - insertGrow
    # Expected sizes: 5 5 11 11 11 23 23 23, G.length 23, probeFind -> 4
    G = [None] * 5
    sizes = []
    for w in W:
        G = insertGrow(G, w)
        sizes.append(len(G))

    print()
    print("sizes                   ->", *sizes)
    print("len(G)                  ->", len(G))
    print("probeFind(G, 'ARE')     ->", probeFind(G, 'ARE'))


# Export list - the Python equivalent of module.exports
__all__ = [
    "num", "h", "chainedTable", "probeInsert", "probeFind", "probeRemove",
    "DELETED", "remove", "doubleHashInsert", "doubleHashFind",
    "maxComparisons", "insertGrow",
]