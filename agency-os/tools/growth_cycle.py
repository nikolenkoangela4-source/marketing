#!/usr/bin/env python3
"""Provider-neutral Instagram baseline, snapshot and decision tools. No network writes."""
import argparse
import json
import math
import statistics
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.0"
METRICS = {"reach": "media_reach", "views": "media_views", "shares": "media_shares",
           "saves": "media_saved", "comments": "media_comments_count", "likes": "media_like_count"}


def instant(value):
    if not value:
        raise ValueError("A source timestamp is required")
    dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    # Windsor data_fetched_at is UTC, sometimes supplied without an offset.
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


def number(value):
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValueError("Boolean is not a count")
    out = float(value)
    if not math.isfinite(out) or out < 0:
        raise ValueError("Counts must be finite and non-negative")
    return out


def rate(numerator, denominator):
    numerator, denominator = number(numerator), number(denominator)
    return None if numerator is None or denominator in (None, 0) else numerator / denominator * 1000


def median(values):
    values = [x for x in values if x is not None]
    return statistics.median(values) if values else None


def normalize(payload):
    rows = payload.get("data")
    if not isinstance(rows, list):
        raise ValueError("Expected an export containing a data list; pending/error is not data")
    seen, out = set(), []
    for row in rows:
        media_id = str(row.get("media_id") or "")
        if not media_id or media_id in seen:
            raise ValueError("Missing or duplicate media_id; do not sum duplicate lifetime rows")
        seen.add(media_id)
        published = instant(row.get("timestamp"))
        captured = instant(row.get("data_fetched_at") or payload.get("captured_at"))
        if captured < published:
            raise ValueError("Snapshot precedes publication")
        kind = row.get("media_type")
        if kind == "REEL" or row.get("media_product_type") == "REELS":
            kind = "REELS"
        item = {"media_id": media_id, "format": kind, "published_at": published.isoformat(),
                "captured_at": captured.isoformat(), "age_hours": (captured-published).total_seconds()/3600,
                "permalink": row.get("media_permalink")}
        for name, field in METRICS.items():
            item[name] = number(row.get(field))
        for name in ("shares", "saves", "comments"):
            item[name + "_per_1000_reached"] = rate(item[name], item["reach"])
        out.append(item)
    return out


def baseline(payload, since, min_age_hours=168):
    normalized = normalize(payload)
    recent = [r for r in normalized if r["published_at"][:10] >= since]
    matured = [r for r in recent if r["age_hours"] >= min_age_hours]
    cohorts = {}
    for kind in sorted({r["format"] for r in recent}, key=str):
        group = [r for r in matured if r["format"] == kind]
        fields = ("reach", "views", "shares_per_1000_reached", "saves_per_1000_reached", "comments_per_1000_reached")
        cohorts[kind] = {"n": len(group), "media_ids": [r["media_id"] for r in group],
                        "medians": {k: median([r[k] for r in group]) for k in fields},
                        "available_n": {k: sum(r[k] is not None for r in group) for k in fields}}
    return {"schema_version": 1, "engine_version": VERSION, "since": since,
            "min_age_hours": min_age_hours, "source_rows": len(normalized), "recent_rows": len(recent),
            "mature_rows": len(matured), "cohorts": cohorts,
            "comparison": "mature_lifetime_context_not_matched_age",
            "limitations": ["Mixed content age", "Trial/paid/collaboration status not established",
                            "Rates are observational; they do not establish causality",
                            "Daily reach sums are not period-unique reach"]}


def record(experiment, payload):
    pub = experiment.get("publication") or {}
    if not pub.get("media_id") or not pub.get("published_at"):
        raise ValueError("Register a real media_id and published_at before recording")
    rows = [r for r in normalize(payload) if r["media_id"] == str(pub["media_id"])]
    if len(rows) != 1:
        raise ValueError("The exact published media_id was not found")
    row = rows[0]
    if instant(row["published_at"]) != instant(pub["published_at"]):
        raise ValueError("Publication timestamp does not match source")
    if row["format"] != experiment["format"]:
        raise ValueError("Published format differs from the registered test")
    return {"schema_version": 1, "experiment_id": experiment["id"], "source": "Windsor.ai Instagram",
            "engine_version": VERSION, **row}


def decide(experiment, snapshots, now):
    if experiment.get("primary_metric") not in ("saves_per_1000_reached", "shares_per_1000_reached"):
        raise ValueError("Unsupported primary metric; do not silently substitute another one")
    result = {"experiment_id": experiment["id"], "decision": "WAITING_PUBLICATION",
              "decision_basis": "preregistered_operating_target", "causal_claim": False,
              "matched_age_winner": False, "engine_version": VERSION}
    pub = experiment.get("publication") or {}
    if not pub.get("media_id") or not pub.get("published_at"):
        return {**result, "reason": "No real publication registered"}
    if experiment.get("design_type") != "prospective_observational_test":
        raise ValueError("Prospective decisions require a prospective manifest")
    if instant(experiment["rules_locked_at"]) > instant(pub["published_at"]):
        raise ValueError("Decision rules were not locked before publication")
    now = instant(now)
    rules = experiment["decision_rules"]
    actual_age = (now-instant(pub["published_at"])).total_seconds()/3600
    if actual_age < rules["target_age_hours"]:
        return {**result, "decision": "WAITING_MATURITY", "reason": "Target content age not reached"}
    valid = []
    for row in snapshots:
        if row.get("experiment_id") != experiment["id"] or row.get("media_id") != str(pub["media_id"]):
            raise ValueError("Snapshot belongs to another experiment/media")
        if row.get("published_at") and instant(row["published_at"]) != instant(pub["published_at"]):
            raise ValueError("Snapshot publication timestamp mismatch")
        captured = instant(row["captured_at"])
        age = (captured-instant(pub["published_at"])).total_seconds()/3600
        if captured > now:
            raise ValueError("Snapshot is dated in the future")
        if rules["target_age_hours"] <= age <= rules["target_age_hours"] + rules["tolerance_hours"]:
            valid.append((captured, row))
    if not valid:
        return {**result, "decision": "INCONCLUSIVE", "reason": "No source-fresh snapshot in the target-age window"}
    _, row = min(valid, key=lambda pair: pair[0])
    metric = experiment["primary_metric"]
    value = rate(row.get("saves" if metric == "saves_per_1000_reached" else "shares"), row.get("reach"))
    result.update({"observed": value, "target": rules["target_rate"], "snapshot_at": row["captured_at"]})
    if value is None:
        return {**result, "decision": "INCONCLUSIVE", "reason": "Missing metric or zero reach"}
    if number(row.get("reach")) < rules["minimum_reach"]:
        return {**result, "decision": "RETEST", "reason": "Insufficient distribution for an operating decision"}
    if value >= rules["target_rate"]:
        return {**result, "decision": "RETEST", "reason": "Operating target met; repeat the mechanism in a new test"}
    return {**result, "decision": "ITERATE", "reason": "Operating target missed; revise hook/value delivery"}


def retrospective(payload, base, media_id):
    rows = [r for r in normalize(payload) if r["media_id"] == str(media_id)]
    if len(rows) != 1:
        raise ValueError("Exact media_id required for retrospective review")
    row = rows[0]
    cohort = base["cohorts"].get(row["format"], {})
    score = row["shares_per_1000_reached"]
    ref = cohort.get("medians", {}).get("shares_per_1000_reached")
    ratio = score/ref if score is not None and ref not in (None, 0) else None
    return {"design_type": "retrospective_review", "media": row, "cohort_n": cohort.get("n", 0),
            "shares_rate_vs_mature_lifetime_median": ratio,
            "decision": "RETEST" if ratio is not None and ratio >= 1.5 and row["reach"] >= 2000 else "ITERATE",
            "decision_basis": "retrospective_prioritization_not_preregistration",
            "causal_claim": False, "follow_conversion_known": False, "matched_age_winner": False,
            "next_action": "Test an original mechanism; inspect the creative before any production reuse"}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    a = sub.add_parser("baseline")
    a.add_argument("--input", required=True); a.add_argument("--since", required=True)
    a.add_argument("--min-age-hours", type=float, default=168); a.add_argument("--out", required=True)
    a = sub.add_parser("record")
    a.add_argument("--experiment", required=True); a.add_argument("--input", required=True); a.add_argument("--out", required=True)
    a = sub.add_parser("decide")
    a.add_argument("--experiment", required=True); a.add_argument("--snapshots", nargs="*", default=[])
    a.add_argument("--now", default=datetime.now(timezone.utc).isoformat()); a.add_argument("--out", required=True)
    a = sub.add_parser("retrospective")
    a.add_argument("--input", required=True); a.add_argument("--baseline", required=True)
    a.add_argument("--media-id", required=True); a.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        if args.command == "baseline":
            result = baseline(read(args.input), args.since, args.min_age_hours)
        elif args.command == "record":
            result = record(read(args.experiment), read(args.input))
        elif args.command == "decide":
            result = decide(read(args.experiment), [read(p) for p in args.snapshots], args.now)
        else:
            result = retrospective(read(args.input), read(args.baseline), args.media_id)
        target = Path(args.out); target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        print(json.dumps({"command": args.command, "output": str(target), "decision": result.get("decision")}, ensure_ascii=False))
    except (ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
