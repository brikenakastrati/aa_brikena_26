from pathlib import Path

#first example: 2 different implemented functions, having the same complexities 
def count_files_iterative(root: str) -> int:
    """
    Count all files under a directory using an explicit stack.

    Parameters
    ----------
    root : str
        Starting directory.

    Returns
    -------
    int
        Total number of files found.

    Complexity
    ----------
    Time: O(N)
        Each of the N filesystem entries is visited once.

    Space: O(D)
        D is the maximum directory depth. The explicit stack can contain
        at most one path per pending directory level in a depth-first walk.
    """
    count = 0
    stack = [Path(root)]

    while stack:
        current = stack.pop()

        if current.is_file():
            count += 1
        elif current.is_dir():
            for child in current.iterdir():
                stack.append(child)

    return count


def count_files_recursive(root: str) -> int:
    """
    Count all files under a directory recursively.

    Parameters
    ----------
    root : str
        Starting directory.

    Returns
    -------
    int
        Total number of files found.

    Complexity
    ----------
    Time: O(N)
        Each of the N filesystem entries is visited once.

    Space: O(D)
        D is the maximum directory depth. The recursive call stack grows
        according to the deepest directory path.

        In Python, this is real stack usage because Python does not perform
        tail-call optimization.
    """
    current = Path(root)

    if current.is_file():
        return 1

    if not current.is_dir():
        return 0

    total = 0

    for child in current.iterdir():
        total += count_files_recursive(str(child))

    return total


#second example: 2 different implemented functions, having different complexities
def unique_ids_iterative(ids: list[int]) -> list[int]:
    """
    Return IDs without duplicates using a set.

    Time complexity: O(n)
    Space complexity: O(n)
    """
    seen = set()
    result = []

    for ticket_id in ids:
        if ticket_id not in seen:
            seen.add(ticket_id)
            result.append(ticket_id)

    return result

def unique_ids_recursive(ids: list[int]) -> list[int]:
    """
    Return IDs without duplicates recursively.

    This version checks whether the first ID appears again in the remaining
    list, then recursively processes the rest.

    Time complexity: O(n^2)
        Each recursive call may scan the remaining list.

    Space complexity: O(n)
        Recursive calls and returned lists grow with the input size.
    """
    if not ids:
        return []

    first_id = ids[0]
    remaining_ids = ids[1:]

    if first_id in remaining_ids:
        return unique_ids_recursive(remaining_ids)

    return [first_id] + unique_ids_recursive(remaining_ids)