"""Problem 2 - Shortest question path (recursive)."""
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


def find_shortest_question_path(questionnaire):
    index = {q["id"]: q for q in questionnaire["questions"]}

    def shortest_from(qid, on_path):
        question = index.get(qid)
        if question is None or qid in on_path:      # unknown id / cycle guard
            return None
        on_path = on_path | {qid}
        best = None
        for answer_id, next_id in branches(question):   # check ALL branches
            prefix_answers = [answer_id] if answer_id else []
            if next_id is None:
                candidate = ([qid], prefix_answers)
            else:
                sub = shortest_from(next_id, on_path)
                if sub is None:
                    continue
                candidate = ([qid] + sub[0], prefix_answers + sub[1])
            if best is None or len(candidate[0]) < len(best[0]):
                best = candidate
        return best

    result = shortest_from(questionnaire["start_question_id"], frozenset())
    if result is None:
        return {"length": 0, "question_ids": [], "answer_path": []}
    ids, answers = result
    return {"length": len(ids), "question_ids": ids, "answer_path": answers}


if __name__ == "__main__":
    data = load_questionnaire()
    result = find_shortest_question_path(data)
    print(json.dumps(result, indent=2))
    assert result["length"] == 4 == len(result["question_ids"])
    assert result["question_ids"] == ["q1", "q5", "q6", "q8"]
    print("OK: shortest path has length 4")
