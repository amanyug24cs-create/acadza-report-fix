import json
import sys

DATA_DIR = "artifacts/file_generation/ttl=63d/intermediate/acadza-report-fix/data"
RESULTS_PATH = "artifacts/file_generation/ttl=63d/intermediate/acadza-report-fix/results.json"

with open(f"{DATA_DIR}/questions.json", "r", encoding="utf-8") as f:
    questions = {q["_id"]: q for q in json.load(f)}
with open(f"{DATA_DIR}/reports.json", "r", encoding="utf-8") as f:
    reports = json.load(f)
with open(f"{DATA_DIR}/taxonomy.json", "r", encoding="utf-8") as f:
    taxonomy = json.load(f)
with open(RESULTS_PATH, "r", encoding="utf-8") as f:
    results = json.load(f)

assert len(results) == 44, f"Expected 44 results, got {len(results)}"
assert [r["reportId"] for r in results] == [r["reportId"] for r in reports], "Order of reportIds must match reports.json"

for res in results:
    rid = res["reportId"]
    qid = res["questionId"]
    assert qid in questions, f"{rid}: Unknown questionId {qid}"
    q = questions[qid]
    qt = q["questionType"]
    q_obj = q[qt]

    verdict = res["verdict"]
    repair = res["repair"]
    edit = res["edit"]
    route = res["route"]

    assert verdict in taxonomy["verdicts"], f"{rid}: Invalid verdict {verdict}"
    assert route in ("auto_apply", "faculty_review", "no_change"), f"{rid}: Invalid route {route}"
    assert 0.0 <= res["confidence"] <= 1.0, f"{rid}: Invalid confidence"
    assert len(res["evidence"]) > 15, f"{rid}: Evidence too short"
    assert len(res["student_reply"]) > 15, f"{rid}: Student reply too short"

    if verdict != "defect":
        assert repair is None, f"{rid}: Non-defect verdict {verdict} must have repair=None"
        assert edit is None, f"{rid}: Non-defect verdict {verdict} must have edit=None"
        assert route == "no_change", f"{rid}: Non-defect verdict {verdict} must have route=no_change"
    else:
        assert repair in taxonomy["repairs"], f"{rid}: Invalid repair {repair}"
        rep_spec = taxonomy["repairs"][repair]
        allowed_fields = rep_spec["fields"]
        is_auto_allowed = rep_spec["auto"]

        if not is_auto_allowed:
            assert route == "faculty_review", f"{rid}: Repair {repair} has auto=False, must route to faculty_review"
            assert edit is None, f"{rid}: Repair {repair} has fields=[], edit must be None"
        else:
            assert edit is not None, f"{rid}: Repair {repair} must provide a surgical edit"
            field = edit["field"]
            assert field in allowed_fields, f"{rid}: Edit field '{field}' not in allowed fields {allowed_fields} for repair '{repair}'"
            find_val = edit["find"]
            replace_val = edit["replace"]
            if field in ("question", "solution"):
                target_str = q_obj[field]
                assert isinstance(find_val, str) and len(find_val) > 0, f"{rid}: find must be non-empty string"
                assert find_val in target_str, f"{rid}: find substring {repr(find_val)} NOT FOUND in {field} of {qid}!"
                assert find_val != replace_val, f"{rid}: find and replace are identical"
            elif field == "answer":
                target_ans = q_obj["answer"]
                assert find_val == target_ans, f"{rid}: find answer {repr(find_val)} != stored answer {repr(target_ans)}"
            elif field == "questionType":
                assert find_val == qt, f"{rid}: find questionType {repr(find_val)} != stored {repr(qt)}"

print("ALL 44 TRIAGE RESULTS PASSED STRICT SCHEMA, TAXONOMY SCOPE, AND SUBSTRING DIFF GUARDS!")
