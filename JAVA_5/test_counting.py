
from counting import (
    six,
    g,
    comparisonCountingSort,
    distributionCountingSort,
    sortByDate,
    tokenize,
    sortAlbanian,
    resetCounters,
    getCounters,
)

# Task 1
resetCounters()
result = comparisonCountingSort(six, g)

print([item["name"] for item in result])
# ['Gent', 'Blend', 'Fjolla', 'Arta', 'Dita', 'Edon']

print(getCounters())
# {'comparisons': 15, 'passes': 0}

# Task 2
resetCounters()
result = distributionCountingSort(six, g, 5, 10)

print([item["name"] for item in result])
# ['Gent', 'Blend', 'Fjolla', 'Arta', 'Dita', 'Edon']

print(getCounters())
# {'comparisons': 0, 'passes': 1}

numbers = [1003, 1001, 1002, 1001]
print(distributionCountingSort(numbers, lambda x: x, 1001, 1003))
# [1001, 1001, 1002, 1003]

# Task 4
print(tokenize("llamba"))
# [17, 1, 18, 2, 1]

print(tokenize("shtëpi"))
# [27, 28, 8, 22, 13]

resetCounters()

words = [
    "shi", "caj", "llamba", "zemër", "dhe", "gur",
    "nënë", "tokë", "xhami", "emër", "rrugë", "cep",
    "ëndërr", "drita", "thikë", "lule", "njeri",
    "gjak", "zhurmë", "rosa", "dera", "sot", "xixa",
    "dhelpër",
]

print(sortAlbanian(words))
print(getCounters())


# output:
# ['Gent', 'Blend', 'Fjolla', 'Arta', 'Dita', 'Edon']
# {'comparisons': 15, 'passes': 0}
# ['Gent', 'Blend', 'Fjolla', 'Arta', 'Dita', 'Edon']
# {'comparisons': 0, 'passes': 1}
# [1001, 1001, 1002, 1003]
# [17, 1, 18, 2, 1]
# [27, 28, 8, 22, 13]
# ['caj', 'cep', 'dera', 'drita', 'dhe', 'dhelpër', 'emër', 'ëndërr', 'gur', 'gjak', 'lule', 'llamba','nënë', 'njeri', 'rosa', 'rrugë', 'sot', 'shi', 'tokë', 'thikë', 'xixa', 'xhami', 'zemër', 'zhurmë']
# {'comparisons': 0, 'passes': 6}
    