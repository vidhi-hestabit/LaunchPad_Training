import json
import hashlib
import re

def normalize(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text

def is_valid(sample):
    return (
        isinstance(sample.get("instruction"), str)
        and isinstance(sample.get("input"), str)
        and isinstance(sample.get("output"), str)
        and len(sample["output"].strip()) > 0
    )

def hash_sample(sample):
    key = normalize(sample["instruction"]) + "||" + normalize(sample["input"])
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

with open("raw_data/raw.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

cleaned = []
seen = set()

for s in raw:
    if not is_valid(s):
        continue

    h = hash_sample(s)
    if h in seen:
        continue

    seen.add(h)
    cleaned.append(s)

with open("raw_data/clean.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=2, ensure_ascii=False)

print("Original samples:", len(raw))
print("Clean samples:", len(cleaned))
print("Removed:", len(raw) - len(cleaned))
