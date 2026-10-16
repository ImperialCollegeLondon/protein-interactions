# Protein Interactions from the Literature

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ImperialCollegeLondon/protein-interactions?quickstart=1)

This repository is the starting point for the Protein Interactions project in the ECRI Research Computing and Data Science hackathon. The project instructions are on the [hackathon wiki](https://github.com/ImperialCollegeLondon/prices/wiki/Projects).

## Quickstart

Open a Codespace with the button above, which has everything set up already. Or, with Python 3.10 or later and Git:

```bash
git clone https://github.com/ImperialCollegeLondon/protein-interactions.git
cd protein-interactions
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Contents

* `pmids.txt` contains the PubMed IDs of some papers on the regulation of the tumour suppressor p53 by MDM2 and related proteins. You can use these, or choose your own topic.
* `tables/answer_key.csv` is an empty table for the interactions you record by hand. Other tables of interactions should use the same columns:
    * `protein_a` and `protein_b` are the two proteins.
    * `interaction` is the type of interaction. `protein_a` acts on `protein_b`.
    * `evidence` is the sentence from the abstract that the interaction comes from.
    * `pmid` is the PubMed ID of the paper.
* `tools/europepmc_server.py` is an MCP server which lets Copilot search Europe PMC and read abstracts. It is already set up in `.vscode/mcp.json`.
* `tools/compare.py` compares a table of interactions with your answer key:

    ```bash
    python tools/compare.py tables/answer_key.csv tables/copilot.csv
    ```

* `tools/check_evidence.py` checks that every evidence sentence in a table appears word for word in the abstract it came from:

    ```bash
    python tools/check_evidence.py tables/copilot.csv
    ```

## Data

Abstracts are fetched from [Europe PMC](https://europepmc.org) when they are needed, and kept in a `.cache` folder which is not committed. The copyright of each abstract belongs to its publisher, so don't commit abstracts to the repository.
