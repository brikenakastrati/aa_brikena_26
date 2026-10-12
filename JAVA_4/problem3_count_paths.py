"""Problem 3 - Count all distinct paths (recursive, with cycle detection)."""
import json
import os


def load_questionnaire(path=None):
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "questionnaire.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def branches(question):
    if question.get("answers"):
        return [(a["id"], a.get("next_question_id")) for a in question["answers"]]
    return [(None, question.get("next_question_id"))]


class _CycleFound(Exception):
    pass


def count_all_possible_paths(questionnaire):
    index = {q["id"]: q for q in questionnaire["questions"]}
    memo = {}          # qid -> number of ways to finish from qid (valid because it's a DAG)
    visiting = set()   # questions on the current recursion stack

    def paths(qid):
        if qid is None:                  # null next id = one completed path
            return 1
        if qid in visiting:              # back-edge -> cycle -> infinite paths
            raise _CycleFound
        if qid in memo:
            return memo[qid]
        question = index.get(qid)
        if question is None:             # dangling reference: treat as an end
            return 1
        visiting.add(qid)
        total = sum(paths(next_id) for _, next_id in branches(question))
        visiting.discard(qid)
        memo[qid] = total
        return total

    try:
        return paths(questionnaire["start_question_id"])
    except _CycleFound:
        return -1


if __name__ == "__main__":
    data = load_questionnaire()
    result = count_all_possible_paths(data)
    print("Total paths:", result)
    assert result == 22

    # Cycle test: q9 points back to q1
    import copy
    cyclic = copy.deepcopy(data)
    for q in cyclic["questions"]:
        if q["id"] == "q9":
            q["next_question_id"] = "q1"
    assert count_all_possible_paths(cyclic) == -1
    print("OK: 22 paths, and -1 for a cyclic questionnaire")
