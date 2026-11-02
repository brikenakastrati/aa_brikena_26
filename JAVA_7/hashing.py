"""
TASK 1 - Trace

Steps:
  1. Create hashing.py and type the data.
  2. On paper, before running anything: fill the Predicted column.
  3. Type the functions, then run the five calls IN THIS ORDER.
  4. Write the real result next to your prediction.

All functions follow the lecture slides exactly.
"""

# ---------------------------------------------------------------------------
# DATA - the lecture's example
# ---------------------------------------------------------------------------
W = ['A', 'FOOL', 'AND', 'HIS', 'MONEY',
     'ARE', 'SOON', 'PARTED']

M = 13


# ---------------------------------------------------------------------------
# num · h · chainedTable  (from the lecture slide)
#
# The lecture's hash: a word is the sum of its letters' positions in the
# alphabet (A = 1 ... Z = 26), then mod m. A number is used as it is.
# Open hashing: every cell holds a list, and a new key goes to the end of
# its list.
# ---------------------------------------------------------------------------
def num(key):
    if isinstance(key, (int, float)):
        return key
    s = 0
    for c in key:
        s += ord(c) - 64
    return s


def h(key, m):
    return num(key) % m


def chained_table(keys, m):
    table = []
    for _ in range(m):
        table.append([])
    for k in keys:
        table[h(k, m)].append(k)
    return table


# ---------------------------------------------------------------------------
# probeInsert · probeFind  (from the lecture slide)
#
# Closed hashing with linear probing, as in the lecture. An empty cell is
# None (null). On a collision the key tries the next cell, and after the
# last cell comes cell 0. A search stops at the first empty cell.
# ---------------------------------------------------------------------------
def probe_insert(table, key):
    m = len(table)
    i = h(key, m)
    while table[i] is not None:
        i = (i + 1) % m
    table[i] = key
    return i


def probe_find(table, key):
    m = len(table)
    i = h(key, m)
    while table[i] is not None:
        if table[i] == key:
            return i
        i = (i + 1) % m
    return -1


# probeRemove (from the lecture slide)
# The same as probe_find except the highlighted line: when the key is found,
# its cell is emptied.
def probe_remove(table, key):
    m = len(table)
    i = h(key, m)
    while table[i] is not None:
        if table[i] == key:
            table[i] = None
            return i
        i = (i + 1) % m
    return -1


# ---------------------------------------------------------------------------
# Build the probing table
# ---------------------------------------------------------------------------
T = [None] * M
for w in W:
    probe_insert(T, w)


# ---------------------------------------------------------------------------
# The five calls - run IN THIS ORDER
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Hashes:", {w: h(w, M) for w in W})
    print("Table T:", T)
    print()
    print("chained_table(W, 13)[11] ->", chained_table(W, 13)[11])
    print("probe_find(T, 'PARTED')  ->", probe_find(T, 'PARTED'))
    print("probe_find(T, 'KID')     ->", probe_find(T, 'KID'))
    print("probe_remove(T, 'ARE')   ->", probe_remove(T, 'ARE'))
    print("probe_find(T, 'SOON')    ->", probe_find(T, 'SOON'))