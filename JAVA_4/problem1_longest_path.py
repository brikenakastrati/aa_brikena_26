"""Problem 1 - Longest question path (recursive)."""
import json
import os


def load_questionnaire(path=None):
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "questionnaire.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def branches(question):
    """Return [(answer_id or None, next_question_id or None), ...] for a question.
    radio/select -> one branch per answer (answer_id is recorded)
    text/checkbox -> a single unconditional branch (no answer_id)."""
    if question.get("answers"):
        return [(a["id"], a.get("next_question_id")) for a in question["answers"]]
    return [(None, question.get("next_question_id"))]


def find_longest_question_path(questionnaire):
    index = {q["id"]: q for q in questionnaire["questions"]}

    def longest_from(qid, on_path):
        """Best (question_ids, answer_ids) starting at qid, or None if no
        valid path exists (e.g. every branch loops back onto the current path)."""
        question = index.get(qid)
        if question is None or qid in on_path:      # unknown id / cycle guard
            return None
        on_path = on_path | {qid}                   # new set -> no manual undo needed
        best = None
        for answer_id, next_id in branches(question):
            prefix_answers = [answer_id] if answer_id else []
            if next_id is None:                     # questionnaire ends here
                candidate = ([qid], prefix_answers)
            else:
                sub = longest_from(next_id, on_path)    # recursive step
                if sub is None:
                    continue
                candidate = ([qid] + sub[0], prefix_answers + sub[1])
            if best is None or len(candidate[0]) > len(best[0]):
                best = candidate
        return best

    result = longest_from(questionnaire["start_question_id"], frozenset())
    if result is None:
        return {"length": 0, "question_ids": [], "answer_path": []}
    ids, answers = result
    return {"length": len(ids), "question_ids": ids, "answer_path": answers}


if __name__ == "__main__":
    data = load_questionnaire()
    result = find_longest_question_path(data)
    print(json.dumps(result, indent=2))
    assert result["length"] == 6 == len(result["question_ids"])
    print("OK: longest path has length 6")
