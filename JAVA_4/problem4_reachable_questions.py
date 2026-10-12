"""Problem 4 - All questions reachable from a given answer (recursive, min depth)."""
import json
import os


def load_questionnaire(path=None):
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "questionnaire.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def next_ids(question):
    """All possible next question ids (ignoring null)."""
    if question.get("answers"):
        ids = [a.get("next_question_id") for a in question["answers"]]
    else:
        ids = [question.get("next_question_id")]
    return [i for i in ids if i is not None]


def find_reachable_questions(questionnaire, question_id, answer_id):
    index = {q["id"]: q for q in questionnaire["questions"]}
    start = index.get(question_id)
    if start is None:
        return []
    answer = next((a for a in start.get("answers", []) if a["id"] == answer_id), None)
    if answer is None:
        return []
    first = answer.get("next_question_id")
    if first is None:
        return []

    best_depth = {}   # qid -> smallest depth seen so far

    def visit(qid, depth):
        if qid not in index:
            return
        if qid in best_depth and best_depth[qid] <= depth:
            return                               # equal/greater depth: stop
        best_depth[qid] = depth                  # new or smaller depth: record...
        for nxt in next_ids(index[qid]):         # ...and recurse again
            visit(nxt, depth + 1)

    visit(first, 1)

    result = [
        {"question_id": qid, "question_text": index[qid]["text"], "min_depth": d}
        for qid, d in best_depth.items()
    ]
    result.sort(key=lambda r: (r["min_depth"], r["question_id"]))
    return result


if __name__ == "__main__":
    data = load_questionnaire()
    res = find_reachable_questions(data, "q2", "a2_truck")
    print(json.dumps(res, indent=2))
    assert [(r["question_id"], r["min_depth"]) for r in res] == [
        ("q4", 1), ("q6", 2), ("q7", 2), ("q8", 3), ("q9", 4)]
    assert find_reachable_questions(data, "q8", "a8_yes") == []
    assert find_reachable_questions(data, "q2", "a9_nope") == []
    print("OK: all three examples match")
