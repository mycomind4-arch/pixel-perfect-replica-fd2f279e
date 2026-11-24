"""Local metadata catalog; no network operations."""
import argparse
import hashlib
import json
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path

def connect(path):
    db = sqlite3.connect(path)
    db.execute("""CREATE TABLE IF NOT EXISTS articles (
        source_sha TEXT NOT NULL, subject TEXT NOT NULL, posted INTEGER,
        groups_json TEXT NOT NULL, message_id TEXT NOT NULL,
        segment_number INTEGER, bytes INTEGER,
        PRIMARY KEY(source_sha, message_id))""")
    return db

def import_nzb(db, path):
    raw = Path(path).read_bytes()
    if len(raw) > 64 * 1024 * 1024:
        raise ValueError("NZB exceeds 64 MiB")
    if b"<!DOCTYPE" in raw.upper() or b"<!ENTITY" in raw.upper():
        raise ValueError("DTD/entity declarations not supported")
    digest = hashlib.sha256(raw).hexdigest()
    root = ET.fromstring(raw)
    rows = []
    for f in root.findall("{*}file"):
        groups = json.dumps([g.text for g in f.findall("{*}groups/{*}group")])
        for s in f.findall("{*}segments/{*}segment"):
            mid = (s.text or "").strip()
            if mid:
                rows.append((digest, f.attrib.get("subject", ""), int(f.attrib.get("date", "0")), groups, mid, int(s.attrib.get("number", "0")), int(s.attrib.get("bytes", "0"))))
    with db:
        db.executemany("INSERT OR IGNORE INTO articles VALUES (?,?,?,?,?,?,?)", rows)
    return len(rows)

def search(db, query):
    return db.execute("SELECT DISTINCT subject,posted,groups_json,source_sha FROM articles WHERE instr(lower(subject), lower(?)) > 0 ORDER BY posted LIMIT 500", (query,)).fetchall()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--db", default="archive.sqlite")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("import-nzb").add_argument("path")
    sub.add_parser("search").add_argument("query")
    a = p.parse_args()
    with connect(a.db) as db:
        if a.command == "import-nzb":
            print("Segments processed:", import_nzb(db, a.path))
        else:
            for row in search(db, a.query):
                print(json.dumps(row))
if __name__ == "__main__":
    main()
