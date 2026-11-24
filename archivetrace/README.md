# ArchiveTrace

Read-only historical publication recovery and evidence catalog. First case: NS-001, NetSender papers. This project is independent of the existing frontend.

## First objective
Recover public article metadata and original publications from alt.binaries.test, 2009. Search publication names rather than attempting to identify private individuals. Preserve original message IDs, timestamps and provenance locally. No attempts to decrypt protected third-party archives.

## Evidence status
Research lead: a March 2009 forum reference to A NeoJungian Grimoire: https://forums.somethingawful.com/showthread.php?threadid=3001925&userid=116171 . Recheck the primary source before publication. User recollections: NetSender alias, Unveiling ESPTech successor, daily inventories, late-2009 cessation. No original manuscripts or successor publication verified. No evidence of deliberate suppression or operational ESP technology.

## Recovery plan
1. Import public NZB files and NNTP overview exports into local SQLite.
2. Use an authorized long-retention NNTP account to check group and header retention; never commit credentials.
3. Search exact publication titles and date ranges, preserving source metadata.
4. Recover authorized public attachments only, hash and quarantine untrusted content, never execute attachments.
5. Compare documents and record corroboration, contradictions and unknowns.

## Candidate upstream
https://github.com/Tensai75/nzbsearcher (license and compatibility review required before reuse).

## Run initial local catalog
Python 3.9+: `python3 catalog.py --db archive.sqlite import-nzb example.nzb` then `python3 catalog.py --db archive.sqlite search NeoJungian`.

The initial catalog does not connect to NNTP or claim any live recovery. Keep database files and recovered content outside Git. This repository is public.
