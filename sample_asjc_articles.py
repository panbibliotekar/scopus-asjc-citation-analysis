#!/usr/bin/env python3
"""Reproducible, year-stratified Scopus sampling for blinded ASJC assessment.

Usage: python sample_asjc_articles.py --input-dir /path/to/scopus_csv --output-dir /path/to/output
No third-party dependencies. Uses SHA-256 keyed by a fixed seed, not Python's
version-dependent pseudo-random sampling internals. Input order is irrelevant.
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

SEED = 20261103
QUOTAS = {2022: 3, 2023: 3, 2024: 2, 2025: 2}
JOURNALS = (
    'Environmental Economics',
    'Innovative Marketing',
    'Knowledge and Performance Management',
    'Mining of Mineral Deposits',
    'Ukrainian Geographical Journal',
)
REQUIRED = {'Title', 'Year', 'Source title', 'Document Type', 'EID', 'Abstract', 'Author Keywords'}


def score(*parts):
    payload = '\x1f'.join(map(str, (SEED, *parts)))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def write_csv(path, columns, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def clean_abstract(value):
    # Scopus appends copyright/publisher boilerplate to many abstracts.
    # Remove the trailing notice to avoid inadvertently revealing the journal.
    return re.split(r"\s*©\s*", value.strip(), maxsplit=1)[0].strip()


def run(input_dir, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    selected = []
    audit = []
    all_eids = set()
    for journal in JOURNALS:
        path = input_dir / f'{journal}.csv'
        if not path.is_file():
            raise FileNotFoundError(f'Missing input file: {path}')
        with path.open(encoding='utf-8-sig', newline='') as handle:
            reader = csv.DictReader(handle)
            missing = REQUIRED - set(reader.fieldnames or [])
            if missing:
                raise ValueError(f'{path.name}: missing columns {sorted(missing)}')
            records = list(reader)
        eligible = []
        local_eids = set()
        for row in records:
            if row['Year'].strip() not in {str(y) for y in QUOTAS}:
                continue
            if row['Document Type'].strip().lower() not in ('article', 'review'):
                continue
            eid = row['EID'].strip()
            if not eid or not row['Title'].strip() or not row['Abstract'].strip():
                raise ValueError(f'{path.name}: eligible record missing EID, title, or abstract')
            if eid in local_eids or eid in all_eids:
                raise ValueError(f'Duplicate Scopus EID: {eid}')
            local_eids.add(eid)
            all_eids.add(eid)
            if row['Source title'].strip().casefold() != journal.casefold():
                raise ValueError(f'{path.name}: unexpected Source title for EID {eid}')
            eligible.append(row)
        for year, quota in QUOTAS.items():
            pool = [r for r in eligible if int(r['Year']) == year]
            if len(pool) < quota:
                raise ValueError(f'{journal}, {year}: {len(pool)} eligible; need {quota}')
            # Stable pseudorandom ordering by a seeded cryptographic hash of EID.
            ranked = sorted(pool, key=lambda r: (score('select', journal, year, r['EID'].strip()), r['EID']))
            picks = ranked[:quota]
            selected.extend({'journal': journal, **r} for r in picks)
            audit.append({'Journal': journal, 'Year': year, 'Eligible records': len(pool), 'Selected records': quota})
    if len(selected) != 50:
        raise AssertionError('Expected exactly 50 records')
    # Independent, deterministic shuffle; anonymised IDs carry no journal/year signal.
    selected.sort(key=lambda r: (score('shuffle', r['EID'].strip()), r['EID']))
    blind = []
    key = []
    for i, row in enumerate(selected, 1):
        article_id = f'A{i:03d}'
        blind.append({
            'Article ID': article_id,
            'Title': row['Title'].strip(),
            'Abstract': clean_abstract(row['Abstract']),
            'Author Keywords': row['Author Keywords'].strip(),
            'Primary ASJC code': '',
            'Secondary ASJC code (optional)': '',
            'Confidence (High/Medium/Low)': '',
            'Comments (optional)': '',
        })
        key.append({
            'Article ID': article_id, 'Journal': row['journal'],
            'Year': row['Year'], 'Document Type': row['Document Type'],
            'EID': row['EID'], 'DOI': row.get('DOI', ''),
            'Title': row['Title'], 'Source title': row['Source title'],
        })
    write_csv(output_dir / 'articles_for_ophelie.csv', list(blind[0]), blind)
    write_csv(output_dir / 'internal_article_key_DO_NOT_SHARE.csv', list(key[0]), key)
    write_csv(output_dir / 'sampling_audit.csv', list(audit[0]), audit)
    manifest = {
        'seed': SEED,
        'selection_algorithm': 'SHA256(seed, select, journal, year, Scopus EID), ascending; first quota records',
        'shuffle_algorithm': 'SHA256(seed, shuffle, Scopus EID), ascending',
        'input_files': [f'{j}.csv' for j in JOURNALS],
        'document_types': ['Article', 'Review'],
        'year_quotas_per_journal': QUOTAS,
        'total_selected': len(selected),
        'eligible_total': sum(r['Eligible records'] for r in audit),
        'notes': [
            'Blinding removes bibliographic identifiers and journal fields, not possible identifying clues within titles/abstracts/keywords.',
            'Scopus copyright boilerplate beginning with © is removed from the blind abstract.',
            'Inspect blind file for remaining journal names or other identifying clues before sharing.',
            'Keep the internal key private until independent coding is complete.',
        ],
    }
    (output_dir / 'sampling_manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f"Selected {len(selected)} of {manifest['eligible_total']} eligible records; outputs in {output_dir}")
    for r in audit:
        print(f"{r['Journal']} | {r['Year']}: {r['Selected records']}/{r['Eligible records']}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir', type=Path, default=Path('.'))
    parser.add_argument('--output-dir', type=Path, default=Path('sampling_output'))
    args = parser.parse_args()
    run(args.input_dir, args.output_dir)
