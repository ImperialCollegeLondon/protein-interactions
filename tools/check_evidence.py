"""Check that every evidence sentence appears word for word in its abstract.

Usage: python tools/check_evidence.py tables/copilot.csv

Differences in spacing and in the style of quotation marks and dashes are
ignored. Exits with an error if any row fails, so it can be used in a hook.
"""

import csv
import re
import sys

from europepmc import get_paper

SUBSTITUTIONS = {"‘": "'", "’": "'", "“": '"', "”": '"',
                 "–": "-", "—": "-", " ": " "}


def normalise(text: str) -> str:
    for old, new in SUBSTITUTIONS.items():
        text = text.replace(old, new)
    text = re.sub(r"<[^>]+>", "", text)  # Europe PMC abstracts can contain HTML tags
    return re.sub(r"\s+", " ", text).strip().lower()


def main(path: str) -> int:
    failures = 0
    with open(path, newline="", encoding="utf-8-sig") as f:
        for line, row in enumerate(csv.DictReader(f), start=2):
            evidence = normalise(row.get("evidence", ""))
            if not evidence:
                print(f"Line {line}: no evidence sentence")
                failures += 1
                continue
            try:
                abstract = normalise(get_paper(row["pmid"].strip())["abstract"])
            except Exception as error:  # report the row and carry on
                print(f"Line {line}: could not fetch the abstract of {row['pmid']}: {error}")
                failures += 1
                continue
            if evidence not in abstract:
                print(f"Line {line}: evidence not found in the abstract of {row['pmid']}")
                failures += 1
    print(f"{failures} row(s) failed" if failures else "All evidence found")
    return 1 if failures else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
