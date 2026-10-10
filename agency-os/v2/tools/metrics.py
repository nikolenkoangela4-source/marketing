"""Local per-row metric calculation; input must be normalized before use."""
import csv, json, sys, math
def number(value):
    if value is None or str(value).strip() == "": return None
    n = float(value)
    if not math.isfinite(n) or n < 0: raise ValueError("Expected finite nonnegative metric")
    return n
def calculate(row):
    m={k:number(row.get(k)) for k in ("reach","views","likes","comments","saves","shares","reposts")}
    def ratio(k, scale=1000):
        return m[k]/m["reach"]*scale if m["reach"] and m[k] is not None else None
    er=None
    if m["reach"] and all(m[k] is not None for k in ("likes","comments","saves","shares")):
        er=sum(m[k] for k in ("likes","comments","saves","shares"))/m["reach"]*100
    return {"media_id":row.get("media_id"),"er_reach_pct":er,
            "shares_per_1000":ratio("shares"),"reposts_per_1000":ratio("reposts"),
            "comments_per_1000":ratio("comments"),"saves_per_1000":ratio("saves"),
            "views_per_reached":ratio("views",1)}
if __name__ == "__main__":
    with open(sys.argv[1], newline="", encoding="utf-8") as f:
        print(json.dumps([calculate(r) for r in csv.DictReader(f)],ensure_ascii=False,indent=2))
