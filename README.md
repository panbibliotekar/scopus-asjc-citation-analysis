# Scopus ASJC Citation Analysis

Reproducible pilot analysis of the ASJC categories of journals citing **Ukrainian Geographical Journal**, designed for extension to 15 Ukrainian journals.

## Scope
- Target publications: 2022–2025.
- Citing publication year: unrestricted.
- **Before exporting citing records from Scopus, apply Source type → Journal.** The notebook assumes this pre-filter; Document Type is not used to determine source type.
- Exclude journal self-citations; keep unmatched and ambiguous records in an audit log.
- Match citing sources by ISSN, then normalized exact source title. Do not automatically accept fuzzy matches.
- A citing source can have several ASJC categories; category percentages are non-exclusive.

## Local files
Place these files under `reference/`:
- `ASJC Classification Codes.xlsx`
- `Scopus_Sources_ASJC_Sep_2026.xlsx`
- `target_journals.xlsx`

Place `ukrainian_geographical_journal.csv` under `input/`.

Run `notebooks/Scopus_ASJC_pilot.ipynb` from the repository root. Results go to `output/`.

## Data availability and provenance
Scopus exports and licensed source lists are **not** committed. Record the Scopus export date, Source List snapshot (September 2026), search query, and input checksums. ASJC codes refer to source classification rather than independent content classification of each citing article.

## Caveat
The percentage of citing journals sharing an ASJC category is an indicator of classification overlap, not proof of an article's topical content.
## Pilot check (25 October 2026)

A user-executed Jupyter PDF export for *Ukrainian Geographical Journal* reports 120 citing journal records, 120 matched, 0 unmatched, 0 ambiguous, and 0 self-citations. Of the target journal's ASJC categories, citing records are distributed as follows (categories may overlap): 1207: 0; 1405: 1; 1900: 5; 1904: 6; 3305: 38. These figures come from the supplied run report; the repository does not include the underlying licensed exports for independent re-execution.

If the CSV is stored outside the repository, set `CITING_FILE` to its actual absolute path in the first notebook code cell, e.g. `Path.home() / "reference/ukrainian_geographical_journal.csv"`. The same variable is reused for provenance hashes. The notebook has not been re-executed after the latest code-review changes.
