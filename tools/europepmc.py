"""Fetch papers from Europe PMC, keeping a local copy of each abstract."""

import json
import pathlib
import urllib.parse
import urllib.request

API = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CACHE = pathlib.Path(__file__).resolve().parent.parent / ".cache"


def _search(query: str, page_size: int, result_type: str) -> list[dict]:
    params = urllib.parse.urlencode(
        {"query": query, "format": "json", "resultType": result_type, "pageSize": page_size}
    )
    with urllib.request.urlopen(f"{API}?{params}", timeout=60) as response:
        return json.loads(response.read())["resultList"]["result"]


def get_paper(pmid: str) -> dict:
    """Return the title, journal, year and abstract of a paper, by PubMed ID."""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / f"{pmid}.json"
    if path.exists():
        return json.loads(path.read_text())
    results = _search(f"EXT_ID:{pmid} AND SRC:MED", 1, "core")
    if not results:
        raise ValueError(f"No paper found with PubMed ID {pmid}")
    paper = results[0]
    record = {
        "pmid": pmid,
        "title": paper.get("title", ""),
        "journal": paper.get("journalInfo", {}).get("journal", {}).get("title", ""),
        "year": paper.get("pubYear", ""),
        "abstract": paper.get("abstractText", ""),
    }
    path.write_text(json.dumps(record, indent=2))
    return record


def search(query: str, max_results: int = 10) -> list[dict]:
    """Search PubMed abstracts on Europe PMC. Returns PubMed IDs, titles and years."""
    results = _search(f"({query}) AND SRC:MED AND HAS_ABSTRACT:Y", max_results, "lite")
    return [{"pmid": r["pmid"], "title": r.get("title", ""), "year": r.get("pubYear", "")} for r in results]
