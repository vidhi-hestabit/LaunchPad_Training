import json
from sklearn.model_selection import train_test_split

with open("raw_data/final.json") as f:
    data = json.load(f)

train, val = train_test_split(data, test_size=0.1, random_state=42)

def write_jsonl(data, path):
    with open(path, "w") as f:
        for s in data:
            f.write(json.dumps(s) + "\n")

write_jsonl(train, "data/train.jsonl")
write_jsonl(val, "data/val.jsonl")

print("Train samples:", len(train))
print("Validation samples:", len(val))
