"""Tests for the string-matching algorithms."""

import string_search as s


def main():
    """Run the algorithm demonstrations and print their results."""
    T = "JIM SAW ME IN A BARBERSHOP"
    P = "BARBER"

    print("===== TASK 1 =====")
    print("Shift Table:", list(s.shift_table(P).items()))

    s.reset_counters()
    print("Brute Force:", s.brute_force(T, P))
    print("Counters:", s.get_counters())

    s.reset_counters()
    print("Horspool:", s.horspool(T, P))
    print("Counters:", s.get_counters())

    s.reset_counters()
    print("Horspool 2:", s.horspool2(T, P))
    print("Counters:", s.get_counters())

    print("\n===== FIND ALL =====")
    kur = "Kur ngjite përpjetë, shiko dhe tatëpjetë."

    s.reset_counters()
    print("Kur:", s.find_all(kur, "pjetë"))
    print("Counters:", s.get_counters())

    s.reset_counters()
    print("Banana:", s.find_all("banana", "ana"))
    print("Counters:", s.get_counters())

    print("\n===== HIGHLIGHT =====")
    print(s.highlight(kur, "pjetë"))
    print(s.highlight("banana", "ana"))

    print("\n===== GOOD SUFFIX TABLE =====")
    print("ABCBAB:", s.good_suffix_table("ABCBAB"))
    print("BAOBAB:", s.good_suffix_table("BAOBAB"))
    print("tatëpjetë:", s.good_suffix_table("tatëpjetë"))

    print("\n===== BOYER MOORE =====")
    text1 = "BESS KNEW ABOUT BAOBABS"
    pattern1 = "BAOBAB"

    s.reset_counters()
    print("Boyer Moore 1:", s.boyer_moore(text1, pattern1))
    print("Counters:", s.get_counters())

    text2 = "Shqiptari me armë e shokë, s'i lutet kurkujt mbi tokë."
    pattern2 = "tokë"

    s.reset_counters()
    print("Boyer Moore 2:", s.boyer_moore(text2, pattern2))
    print("Counters:", s.get_counters())

    print("\n===== ADDITIONAL TESTS =====")
    s.reset_counters()
    print("No match:", s.brute_force("hello", "xyz"))
    print("Find All No Match:", s.find_all("hello", "xyz"))
    print("Highlight No Match:", s.highlight("hello", "xyz"))
    print("Empty Pattern:", s.boyer_moore("hello", ""))


if __name__ == "__main__":
    main()
