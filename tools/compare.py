"""Compare a table of interactions with an answer key.

Usage: python tools/compare.py tables/answer_key.csv tables/copilot.csv

Two rows match when they have the same PubMed ID, the same two proteins in the
same order, and the same interaction type. Letter case and spaces around values
are ignored. The evidence column is not compared.
"""

import csv
import sys


def load(path: str) -> set[tuple[str, str, str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return {
            (
                row["pmid"].strip(),
                row["protein_a"].strip().upper(),
                row["protein_b"].strip().upper(),
                row["interaction"].strip().lower(),
            )
            for row in csv.DictReader(f)
        }


def main(key_path: str, other_path: str) -> None:
    key, other = load(key_path), load(other_path)
    if not key:
        sys.exit(f"{key_path} has no rows yet, so there is nothing to compare against.")
    # only compare papers that appear in the answer key
    papers = {row[0] for row in key}
    other = {row for row in other if row[0] in papers}
    found = key & other

    print(f"Papers compared: {len(papers)}")
    print(f"In the answer key: {len(key)}   Found: {len(found)}")
    print(f"Recorded but not in the answer key: {len(other - key)}")
    for label, rows in [("Missed", key - other), ("Extra", other - key)]:
        for pmid, a, b, kind in sorted(rows):
            print(f"  {label}: {pmid}  {a} {kind} {b}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
