



# TASK1: write

# -One file, counting.py written by you. Keep c1, c2, and c3 functions from Task 1 in it. 
# NO .sort() and no localeCompare anywhere in the file 
# counter comparissons: +1 every time two keys are compared. 
# counter passes: +1 for every counting pass (count -> running sums -> place)
# resetCounters() sets both to 0. getCounters() returns a {comparisons, passes}.
# the file ends with exactly this export: 
    
#     module.exports = {
#         c1,
#         c2,
#         c3,
#         comparisonCountingSort,
#         distribtionCountingSort,
#         sortByDate, 
#         tokensize,
#         sortAlbanian, 
#         resetCounters,
#         getCounters
#     }
    
# steps: 
#     1. start from c1 
#     change the comparisson so that on equal keys the alter record gets +1 
#     add comparissons++ once for every pair i<j 
    
# requirements: 
#     returns a new array sorted by key 
#     stable: equal keys keep their input order 
#     A is not changed 
#     Exactly n(n-1)/2 comparisons
    
# check: 
#     comparisonCountingSort(six,g ) -> Gent Blend Fjolla Arta Dita Edon 
#     comparissons after one call on six -> 15
    
# TASK2: write
    
# distributionCountingSort(six,g,lo,hi)

# steps: 
#     1. start from c2 
#     2. D gets hi-lo+1 cells, at 0
#     count: for every element, D[key [x]- lo] +1
#     running sums: D[j] += D[j-1]
#     place: walk A from right to left, put each element at D[j] -1
# then decrease D[j]
# passes++ once per call. 

# requirements: 
#     key returns a whole number in lo...hi 
#     No key is compared with another 
#     Stable. Returns a new array, A is not changed
#     works for any lo, and for an empty array 
    
#     check: 
#   distributionCountingSort(six,g,5,10) -> Gent Blend Fjolla Arta Dita Edon
  
#   distributionCountingSort([1003,1001,1002,1001], (x) => x, 1001, 1003) -> [1001, 1003]
#                                                                             - > [1001, 1001, 1002, 1003]
                                                                            

# TASK3: write
#     sortByDate(records) 
    
# const recs = [
# { id: 0, date: '2024-10-13' }, { id: 1, date: '2024-01-20' }, { id: 2, date: '2026-05-15' },
# { id: 3, date: '2024-01-15' }, { id: 4, date: '2024-05-82' }, { id: 5, date: '2026-08-27' },
# { id: 6, date: "2025-02-19' }, { id: 7, date: "2026-11-22' }, { id: B, date: '2024-09-19' },
# { id: 9, date: '2026-12-11" }
# ]

# STEPS:
# find the smallest and the largest year. 
# distributionCountingSort on the day 1, ... 31. 
# then on the month 1, ... 12.
# then on the year smallest, ... largest.


# REQUIREMENTS:
# exactly three calls passes=3 
# no date string is compared with another
# oldest first. Stable. Returns a new array

# check: sortByDate((recs).map(r) => r.id) -> 3 1 4 8 0 6 2 5 7 9 


# TASK4:write 

# tokenize(word) sortAlbanian(words)

# aphabet: 1-36- albanian letters
# words: shi caj llamba zemer dhe gur nene toke xhami emer rruge cep enderr drita thike lule njeri gjak zhurme rosa dera sot xixa dhelper


# STEPS

# 1. tokenize: read the word left to right. If the next two characters are one
# of dh gj Il nj rr sh th xh zh, they are one letter. Return the letter numbers
# (a=1 ... zh=36).

# 2. sortAlbanian: tokenize every word, find the longest one.
# 3. One distributionCountingSort per letter position, last position first,
# range 0 .. 36. A word with no letter at that position gets 0.


# REQUIRENENTS
# - Dictionary order, not .sort () order.
# - One pass per letter position: 6 for these words.

# - Retums a new array.

# check: 
# tokenize('llamba') - [17, 1, 18, 2, 1]
# sortAlbanian(words) + cep çaj dera drita dhe dhelper emer ëndērr .

# tokenize('shtēpi') + [27, 28, 8, 22, 13]



# counting.py
# Counting sorts: comparison counting and distribution counting.
# No built-in sorting and no locale comparison.

six = [
    {"name": "Arta", "grade": 9},
    {"name": "Blend", "grade": 6},
    {"name": "Dita", "grade": 9},
    {"name": "Edon", "grade": 9},
    {"name": "Fjolla", "grade": 6},
    {"name": "Gent", "grade": 5},
]


def g(record):
    """Return the grade of a record."""
    return record["grade"]


# ---- Counters ----

comparisons = 0
passes = 0


def resetCounters():
    """Reset both counters to zero."""
    global comparisons, passes
    comparisons = 0
    passes = 0


def getCounters():
    """Return the current comparison and pass counters."""
    return {"comparisons": comparisons, "passes": passes}


# ---- Task 1: Original functions ----

def c1(A, key):
    """Comparison counting sort; equal keys are not guaranteed stable."""
    n = len(A)
    count = [0] * n

    for i in range(n - 1):
        for j in range(i + 1, n):
            if key(A[i]) < key(A[j]):
                count[j] += 1
            else:
                count[i] += 1

    S = [None] * n
    for i in range(n):
        S[count[i]] = A[i]

    return S


def c2(A, key, lo, hi):
    """Stable distribution counting sort, placing right to left."""
    D = [0] * (hi - lo + 1)

    for item in A:
        D[key(item) - lo] += 1

    for j in range(1, len(D)):
        D[j] += D[j - 1]

    S = [None] * len(A)

    for i in range(len(A) - 1, -1, -1):
        j = key(A[i]) - lo
        S[D[j] - 1] = A[i]
        D[j] -= 1

    return S


def c3(A, key, lo, hi):
    """Distribution counting sort, placing left to right."""
    D = [0] * (hi - lo + 1)

    for item in A:
        D[key(item) - lo] += 1

    for j in range(1, len(D)):
        D[j] += D[j - 1]

    S = [None] * len(A)

    for item in A:
        j = key(item) - lo
        S[D[j] - 1] = item
        D[j] -= 1

    return S

#Output: 
#c1 ['Gent', 'Fjolla', 'Blend', 'Edon', 'Dita', 'Arta']- did not save the original order of the records with the same grade
#c2 ['Gent', 'Blend', 'Fjolla', 'Arta', 'Dita', 'Edon']- stable sort
#c3 ['Gent', 'Fjolla', 'Blend', 'Edon', 'Dita', 'Arta']- did not save the original order of the records with the same grade


# ---- Task 1: Stable comparison counting sort ----

def comparisonCountingSort(A, key):
    """
    Sort records by key using comparison counting.

    Equal keys preserve their original input order.
    The input list is not modified.
    """
    global comparisons

    n = len(A)
    count = [0] * n

    for i in range(n - 1):
        for j in range(i + 1, n):
            comparisons += 1

            if key(A[i]) <= key(A[j]):
                # A[i] precedes A[j], including when keys are equal.
                count[j] += 1
            else:
                count[i] += 1

    S = [None] * n

    for i in range(n):
        S[count[i]] = A[i]

    return S


# ---- Task 2: Stable distribution counting sort ----

def distributionCountingSort(A, key, lo, hi):
    """
    Sort records by integer key using stable distribution counting.

    Keys must be integers in the inclusive range [lo, hi].
    The input list is not modified.
    """
    global passes
    passes += 1

    D = [0] * (hi - lo + 1)

    # Count occurrences of each key.
    for item in A:
        D[key(item) - lo] += 1

    # Calculate cumulative counts.
    for j in range(1, len(D)):
        D[j] += D[j - 1]

    # Place items from right to left to preserve stability.
    S = [None] * len(A)

    for i in range(len(A) - 1, -1, -1):
        j = key(A[i]) - lo
        S[D[j] - 1] = A[i]
        D[j] -= 1

    return S


# ---- Task 3: Sort dates, oldest first ----

def _parse_date(date_string):
    """Convert YYYY-MM-DD into integer year, month, and day."""
    year, month, day = date_string.split("-")
    return int(year), int(month), int(day)


def sortByDate(records):
    """
    Return records sorted by date, oldest first.

    Uses three stable distribution-counting passes:
    day, month, then year.
    """
    if len(records) == 0:
        return []

    dated = [
        (record, _parse_date(record["date"]))
        for record in records
    ]

    min_year = dated[0][1][0]
    max_year = dated[0][1][0]

    for _, date_parts in dated:
        year = date_parts[0]

        if year < min_year:
            min_year = year

        if year > max_year:
            max_year = year

    # Least significant component first.
    result = distributionCountingSort(
        dated, lambda item: item[1][2], 1, 31
    )
    result = distributionCountingSort(
        result, lambda item: item[1][1], 1, 12
    )
    result = distributionCountingSort(
        result, lambda item: item[1][0], min_year, max_year
    )

    return [item[0] for item in result]


# ---- Task 4: Albanian dictionary order ----

LETTERS = [
    "a", "b", "c", "ç", "d", "dh", "e", "ë", "f", "g",
    "gj", "h", "i", "j", "k", "l", "ll", "m", "n", "nj",
    "o", "p", "q", "r", "rr", "s", "sh", "t", "th", "u",
    "v", "x", "xh", "y", "z", "zh",
]

LETTER_NUMBER = {
    letter: index + 1
    for index, letter in enumerate(LETTERS)
}

DIGRAPHS = (
    "dh", "gj", "ll", "nj", "rr",
    "sh", "th", "xh", "zh",
)


def tokenize(word):
    """
    Convert a word into Albanian alphabet letter numbers.

    Digraphs count as single letters.
    """
    word = word.lower().replace("ē", "ë")
    result = []
    i = 0

    while i < len(word):
        two_letters = word[i:i + 2]

        if two_letters in DIGRAPHS:
            result.append(LETTER_NUMBER[two_letters])
            i += 2
        else:
            result.append(LETTER_NUMBER[word[i]])
            i += 1

    return result


def sortAlbanian(words):
    """
    Sort words according to Albanian dictionary order.

    Uses one stable distribution-counting pass per letter
    position, starting at the last position.
    """
    if len(words) == 0:
        return []

    items = [(word, tokenize(word)) for word in words]

    longest = 0

    for _, tokens in items:
        if len(tokens) > longest:
            longest = len(tokens)

    result = items

    for position in range(longest - 1, -1, -1):
        result = distributionCountingSort(
            result,
            lambda item, pos=position: (
                item[1][pos] if pos < len(item[1]) else 0
            ),
            0,
            36,
        )

    return [item[0] for item in result]


# ---- Required assignment names ----

distribtionCountingSort = distributionCountingSort
tokensize = tokenize

__all__ = [
    "c1",
    "c2",
    "c3",
    "comparisonCountingSort",
    "distribtionCountingSort",
    "sortByDate",
    "tokensize",
    "sortAlbanian",
    "resetCounters",
    "getCounters",
]
