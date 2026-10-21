"""String matching algorithms: Brute Force, Horspool, and Boyer-Moore."""

# =====================================
# COUNTERS
# =====================================

comparisons = 0
alignments = 0


def reset_counters():
    """Reset comparison and alignment counters."""
    global comparisons, alignments
    comparisons = 0
    alignments = 0


def get_counters():
    """Return the current comparison and alignment counts."""
    return {"comparisons": comparisons, "alignments": alignments}


# =====================================
# 1. BRUTE FORCE
# =====================================

def brute_force(T, P):
    """Return the first index of P in T using brute-force matching."""
    global comparisons, alignments

    n, m = len(T), len(P)
    if m == 0:
        return 0

    for i in range(n - m + 1):
        alignments += 1
        j = 0

        while j < m:
            comparisons += 1
            if P[j] != T[i + j]:
                break
            j += 1

        if j == m:
            return i

    return -1


# =====================================
# 2. SHIFT TABLE
# =====================================

def shift_table(P):
    """Build the Horspool bad-character shift table for pattern P."""
    m = len(P)
    table = {}

    for j in range(m - 1):
        table[P[j]] = m - 1 - j

    return table


def shift(table, c, m):
    """Return the shift distance for character c."""
    return table[c] if c in table else m


# =====================================
# 3. HORSPOOL
# =====================================

def horspool(T, P):
    """Return the first index of P in T using Horspool matching."""
    global comparisons, alignments

    n, m = len(T), len(P)
    if m == 0:
        return 0

    table = shift_table(P)
    i = m - 1

    while i <= n - 1:
        alignments += 1
        k = 0

        while k < m:
            comparisons += 1
            if P[m - 1 - k] != T[i - k]:
                break
            k += 1

        if k == m:
            return i - m + 1

        i += shift(table, T[i], m)

    return -1


# =====================================
# 4. HORSPOOL 2
# =====================================

def horspool2(T, P):
    """Return the first match using the alternative Horspool shift."""
    global comparisons, alignments

    n, m = len(T), len(P)
    if m == 0:
        return 0

    table = shift_table(P)
    i = m - 1

    while i <= n - 1:
        alignments += 1
        k = 0

        while k < m:
            comparisons += 1
            if P[m - 1 - k] != T[i - k]:
                break
            k += 1

        if k == m:
            return i - m + 1

        i += shift(table, T[i - k], m)

    return -1


# =====================================
# 5. FIND ALL
# =====================================

def find_all(T, P):
    """Return all match start indices using a Horspool-style search."""
    global comparisons, alignments

    result = []
    n, m = len(T), len(P)

    if m == 0:
        return result

    table = shift_table(P)
    i = m - 1

    while i <= n - 1:
        alignments += 1
        k = 0

        while k < m:
            comparisons += 1
            if P[m - 1 - k] != T[i - k]:
                break
            k += 1

        if k == m:
            result.append(i - m + 1)

        # Shift even after finding a match.
        i += shift(table, T[i], m)

    return result


# =====================================
# 6. HIGHLIGHT
# =====================================

def highlight(T, P):
    """Surround non-overlapping occurrences of P in T with brackets."""
    if len(P) == 0:
        return T

    positions = find_all(T, P)
    result = []
    i = 0
    match_index = 0

    while i < len(T):
        # Skip overlapping matches.
        while (
            match_index < len(positions)
            and positions[match_index] < i
        ):
            match_index += 1

        if (
            match_index < len(positions)
            and positions[match_index] == i
        ):
            result.append("[")
            result.append(T[i:i + len(P)])
            result.append("]")
            i += len(P)
            match_index += 1
        else:
            result.append(T[i])
            i += 1

    return "".join(result)


# =====================================
# 7. GOOD SUFFIX TABLE
# =====================================

def good_suffix_table(P):
    """Build the good-suffix shift table used by Boyer-Moore."""
    m = len(P)
    d2 = [0] * m

    for k in range(1, m):
        suffix_start = m - k
        found = -1

        # Find the rightmost earlier occurrence of the suffix.
        for s in range(suffix_start - 1, -1, -1):
            same = True

            for j in range(k):
                if P[s + j] != P[suffix_start + j]:
                    same = False
                    break

            if (
                same
                and (
                    s == 0
                    or P[s - 1] != P[suffix_start - 1]
                )
            ):
                found = s
                break

        if found != -1:
            d2[k] = suffix_start - found
            continue

        # Find the longest prefix that is also a suffix.
        longest = 0

        for size in range(k - 1, 0, -1):
            same = True

            for j in range(size):
                if P[j] != P[m - size + j]:
                    same = False
                    break

            if same:
                longest = size
                break

        d2[k] = m - longest

    return d2


# =====================================
# 8. BOYER-MOORE
# =====================================

def boyer_moore(T, P):
    """Return the first index of P in T using Boyer-Moore matching."""
    global comparisons, alignments

    n, m = len(T), len(P)
    if m == 0:
        return 0

    t1 = shift_table(P)
    d2 = good_suffix_table(P)
    i = m - 1

    while i <= n - 1:
        alignments += 1
        k = 0

        while k <= m - 1:
            comparisons += 1
            if P[m - 1 - k] != T[i - k]:
                break
            k += 1

        if k == m:
            return i - m + 1

        c = T[i - k]
        d1 = max(shift(t1, c, m) - k, 1)

        if k == 0:
            i += d1
        else:
            i += max(d1, d2[k])

    return -1
