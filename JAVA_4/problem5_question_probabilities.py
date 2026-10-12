"""Problem 5 - Probability that each question is shown + expected position."""
import json
import os


def load_questionnaire(path=None):
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "questionnaire.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def next_ids(question):
    """One entry per answer (duplicates kept: each answer is its own branch)."""
    if question.get("answers"):
        return [a.get("next_question_id") for a in question["answers"]]
    return [question.get("next_question_id")]


def calculate_question_probabilities(questionnaire):
    index = {q["id"]: q for q in questionnaire["questions"]}
    prob = {qid: 0.0 for qid in index}       # total probability of being shown
    pos_sum = {qid: 0.0 for qid in index}    # sum of probability * position

    def walk(qid, p, position, on_path):
        """Push probability p (arriving at `position`) into qid and forward."""
        if qid not in index or qid in on_path:   # unknown id / cycle guard
            return
        prob[qid] += p                           # accumulate across branches
        pos_sum[qid] += p * position
        options = next_ids(index[qid])
        share = p / len(options)                 # equal chance for each answer
        for nxt in options:
            if nxt is not None:
                walk(nxt, share, position + 1, on_path | {qid})

    walk(questionnaire["start_question_id"], 1.0, 1, frozenset())

    result = []
    for qid, q in index.items():
        p = prob[qid]
        expected = pos_sum[qid] / p if p > 0 else 0.0
        result.append({
            "question_id": qid,
            "question_text": q["text"],
            "probability": round(p, 4),
            "expected_position": round(expected, 4),
        })
    result.sort(key=lambda r: (-r["probability"], r["question_id"]))
    return result


if __name__ == "__main__":
    data = load_questionnaire()
    res = calculate_question_probabilities(data)
    for r in res:
        print(f'{r["question_id"]}  p={r["probability"]:<7} pos={r["expected_position"]}')
    total = sum(r["probability"] for r in res)
    print("Sum of probabilities:", round(total, 4))
    assert round(total, 4) == 5.0
    table = {r["question_id"]: (r["probability"], r["expected_position"]) for r in res}
    assert table["q6"] == (0.875, 3.4286)
    assert table["q8"] == (1.0, 4.5)
    assert table["q7"] == (0.125, 4.0)
    print("OK: matches the expected table")
