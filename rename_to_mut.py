#!/usr/bin/env python3
"""Rename FoundHer (women-only) -> MUT (all genders). Audited find/replace."""
import re, sys

path = "/Users/chongkosnitwong/hermes/foundher/index.html"
src = open(path, encoding="utf-8").read()

# (old, new, expected_count)
edits = [
    ("<title>FoundHer — The 6-week bootcamp for women founding businesses in Germany</title>",
     "<title>MUT — The 6-week bootcamp for founding a business in Germany</title>", 1),
    ("content=\"FoundHer is a part-time, 6-week bootcamp for women in Germany. Validate your idea, crack the German paperwork, and launch a registered business — with mentors who've done it.\"",
     "content=\"MUT is a part-time, 6-week bootcamp for first-time founders in Germany. Validate your idea, crack the German paperwork, and launch a registered business — with mentors who've done it.\"", 1),
    ("text-anchor='middle'%3EF.%3C/text%3E", "text-anchor='middle'%3EM%3C/text%3E", 1),
    ('<span class="logo-mark">F.</span>', '<span class="logo-mark">✳</span>', 2),
    ("Found<i>Her</i>", "MUT", 2),
    ('aria-label="FoundHer home"', 'aria-label="MUT home"', 1),
    ("<p class=\"hero-sub\">FoundHer is a part-time bootcamp for women in Germany who are done waiting.",
     "<p class=\"hero-sub\">MUT is a part-time bootcamp for people in Germany who are done waiting.", 1),
    ("FoundHer works best for women at the very beginning",
     "MUT works best for first-time founders at the very beginning", 1),
    ("eleven women who notice", "eleven founders who notice", 1),
    ("<span>Gründerin</span>", "<span>Gründer*innen</span>", 2),
    ("<h3>Sina Katz</h3>", "<h3>Jonas Brandt</h3>", 1),
    ("<div class=\"avatar\">SK</div>", "<div class=\"avatar\">JB</div>", 1),
    ("<footer><b>Amara D.</b> · Catering & events · Cohort 02 · Berlin</footer>",
     "<footer><b>Daniel K.</b> · Street food & catering · Cohort 02 · Köln</footer>", 1),
    ("per cohort for women who need them", "per cohort for founders who need them", 1),
    ("A mom of two.", "A parent of two.", 1),
    ("Twelve women. Six weeks.", "Twelve founders. Six weeks.", 1),
    ("hello@foundher.eu", "hello@mut.camp", 2),
    ("— The FoundHer team", "— Team MUT", 1),
    ("</span> FoundHer · <span", "</span> MUT · <span", 1),
]

report, fail = [], 0
for old, new, exp in edits:
    n = src.count(old)
    if n != exp:
        report.append(f"MISMATCH ({n} found, {exp} expected): {old[:70]}")
        fail += 1
    else:
        src = src.replace(old, new)
        report.append(f"ok x{n}: {old[:60]}")

if fail:
    print("\n".join(report)); print(f"ABORTED: {fail} mismatches — file NOT modified"); sys.exit(1)

open(path, "w", encoding="utf-8").write(src)

leftovers = []
for pat in ["FoundHer", "Found<i>", "women", "Gründerin</span>", "foundher.eu", "Sina Katz", "Amara D."]:
    hits = len(re.findall(re.escape(pat), src))
    if hits: leftovers.append(f"{pat}: {hits} LEFTOVER")
print("\n".join(report)); print("---")
print("leftovers:", leftovers if leftovers else "NONE — clean")
print("title:", re.search(r"<title>(.*?)</title>", src).group(1))
print("html lang:", re.search(r'lang="(\w+)"', src).group(1))
