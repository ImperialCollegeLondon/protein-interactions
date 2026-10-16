"""An MCP server which lets Copilot search for papers and read their abstracts."""

from europepmc import get_paper, search
from mcp.server import MCPServer

mcp = MCPServer("europepmc")


@mcp.tool()
def search_papers(query: str, max_results: int = 10) -> list[dict]:
    """Search PubMed abstracts on Europe PMC.

    The query uses Europe PMC's search syntax, for example "MDM2 AND p53".
    Returns the PubMed ID, title and year of each paper.
    """
    return search(query, max_results)


@mcp.tool()
def get_abstract(pmid: str) -> dict:
    """Return the title, journal, year and abstract of a paper, by its PubMed ID."""
    return get_paper(pmid)


if __name__ == "__main__":
    mcp.run()
