import pandas as pd
import hashlib

# Integrity Checks (Hashing - Detect unexpected changes)
with open("data/processed/extracted-tables_clean.csv", "rb") as f:
    data = f.read()
    sha256hash = hashlib.sha256(data).hexdigest()

with open("hashes/milano_results.sha", "w") as f:
    f.write(sha256hash)

with open("data/olympic_hosts_clean.csv", "rb") as f:
    data = f.read()
    sha256hash = hashlib.sha256(data).hexdigest()

with open("hashes/olympic_hosts.sha", "w") as f:
    f.write(sha256hash)