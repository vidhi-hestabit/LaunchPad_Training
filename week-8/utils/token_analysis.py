import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from transformers import AutoTokenizer
import os 


MODEL_NAME = "microsoft/phi-3-mini-4k-instruct"
MAX_TOKENS = 4096

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

with open("raw_data/clean.json") as f:
    data = json.load(f)

lengths = []

for s in data:
    text = s["instruction"] + s["input"] + s["output"]
    token_count = len(tokenizer(text)["input_ids"])
    lengths.append(token_count)

os.makedirs("data", exist_ok=True)

plt.figure(figsize=(10, 6))
plt.hist(lengths, bins=40)
plt.xlabel("Token Count")
plt.ylabel("Frequency")
plt.title("HR Dataset Token Distribution")
plt.tight_layout()
plt.savefig("data/DATASET_TOKEN_DISTRIBUTION.png")
plt.close()

print("Max tokens:", max(lengths))
print("Average tokens:", sum(lengths) / len(lengths))

filtered = [
    s for s in data
    if len(tokenizer(s["instruction"] + s["input"] + s["output"])["input_ids"]) <= MAX_TOKENS
]

with open("raw_data/final.json", "w") as f:
    json.dump(filtered, f, indent=2)

print("Final dataset size:", len(filtered))
