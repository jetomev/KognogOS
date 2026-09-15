import importlib.util, sys
spec = importlib.util.spec_from_file_location(
    "watch", "/home/jetomev/Programs/kognog/scripts/repo-aur-watch.py")
W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)

R = "https://api.github.com/repos/jetomev/demo"
def iss(n, user, title, state="open", closed_at=None, pr=False):
    d = {"number": n, "title": title, "state": state, "closed_at": closed_at,
         "html_url": f"http://x/{n}", "user": {"login": user},
         "created_at": "2026-09-01T00:00:00Z"}
    if pr: d["pull_request"] = {}
    return d
def com(n, user, at):
    return {"issue_url": f"{R}/issues/{n}", "user": {"login": user}, "created_at": at}
def rev(n, user, at):
    return {"pull_request_url": f"{R}/pulls/{n}", "user": {"login": user}, "created_at": at}

ISSUES = [
  iss(1,"outsider","1 outside, never answered"),
  iss(2,"outsider","2 outside, we replied last"),
  iss(3,"outsider","3 outside, they came back after us"),
  iss(4,"jetomev","4 ours, outsider asked a question"),
  iss(5,"jetomev","5 ours, nobody replied"),
  iss(6,"outsider","6 closed AFTER their last word",   "closed","2026-09-05T00:00:00Z"),
  iss(7,"outsider","7 they spoke AFTER we closed",     "closed","2026-09-02T00:00:00Z"),
  iss(8,"outsider","8 last word is a bot"),
  iss(9,"outsider","9 PR, outside review comment last", pr=True),
]
CONV = [
  com(2,"outsider","2026-09-02T00:00:00Z"), com(2,"jetomev","2026-09-03T00:00:00Z"),
  com(3,"jetomev","2026-09-03T00:00:00Z"),  com(3,"outsider","2026-09-04T00:00:00Z"),
  com(4,"outsider","2026-09-04T00:00:00Z"),
  com(6,"outsider","2026-09-04T00:00:00Z"),
  com(7,"outsider","2026-09-09T00:00:00Z"),
  com(8,"jetomev","2026-09-03T00:00:00Z"), com(8,"dependabot[bot]","2026-09-06T00:00:00Z"),
]
REV = [ rev(9,"jetomev","2026-09-03T00:00:00Z"), rev(9,"outsider","2026-09-07T00:00:00Z") ]
CC  = [ {"commit_id":"abc1234deadbeef","user":{"login":"outsider"},
         "body":"10 commit comment from outside","created_at":"2026-09-08T00:00:00Z",
         "html_url":"http://x/c"} ]

def fake(path, paginate=True):
    if path.startswith("user/repos"):
        return [{"name":"demo","archived":False,"owner":{"login":"jetomev"}}]
    if "/issues?" in path: return ISSUES
    if "/issues/comments" in path: return CONV
    if "/pulls/comments" in path: return REV
    if "/demo/comments" in path: return CC
    return []
W.gh_api = fake

waiting, repos = W.collect_github()
got = sorted(w["where"] for w in waiting)
expect = sorted(["demo #1","demo #3","demo #4","demo #7","demo #9","demo abc1234"])
print("FLAGGED AS WAITING:")
for w in sorted(waiting, key=lambda x: x["where"]):
    print(f"   {w['where']:16} {w['kind']:15} by {w['who']:16} {w['what'][:44]}")
print()
print("expected:", expect)
print("got     :", got)
if got == expect:
    print("\n*** PASS — all 10 situations classified correctly ***")
else:
    print("\n*** FAIL ***")
    print("  missed         :", [x for x in expect if x not in got])
    print("  false positives:", [x for x in got if x not in expect])
    sys.exit(1)
