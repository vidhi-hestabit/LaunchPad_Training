
# HR INSTRUCTION TUNING (WEEK 8)

## 1. Domain Selection
**Domain:** Human Resources (HR)

The HR domain was selected because it naturally supports:
- Question Answering (HR concepts, policies)
- Multi-step reasoning (policy justification, decision making)
- Structured information extraction (employee details, leave requests)
---

## 2. Dataset Objective
The goal of this dataset is to instruction-tune a small/medium LLM so it can:
- Act as an HR assistant
- Answer HR-related questions accurately
- Reason about HR policies and practices
- Extract structured HR information from unstructured text
---

## 3. Dataset Format
Each sample follows the standard instruction-tuning JSONL format:

```json
{
  "instruction": "...",
  "input": "...",
  "output": "..."
}
````

This format is compatible with `transformers`, `trl`, and `SFTTrainer`.

---

## 4. Dataset Composition

| Sample Type | Description                     | Approx. Percentage |
| ----------- | ------------------------------- | ------------------ |
| QA          | Direct HR questions and answers | ~40%               |
| Reasoning   | Step-by-step HR explanations    | ~35%               |
| Extraction  | Structured HR data extraction   | ~25%               |

---

## 5. Dataset Size

| Stage                 | Number of Samples |
| --------------------- | ----------------- |
| Raw generated samples | 1000              |
| After cleaning        | ~250              |
| After token filtering | ~250              |
| Training set          | ~216              |
| Validation set        | ~25               |

---

## 6. Data Generation Strategy

The dataset was generated using:

* Parameterized templates
* Controlled randomization
* HR-specific entities such as employee names, roles, policies, and leave types

This ensured:

* High semantic diversity
* Minimal duplication
* Realistic HR scenarios

---

## 7. Data Cleaning Steps

The following cleaning steps were applied:

* Removed samples with missing or empty fields
* Ensured all `instruction`, `input`, and `output` fields are strings
* Preserved controlled repetition to avoid over-pruning
* Maintained semantic diversity across samples

---

## 8. Token Length Analysis

Tokenization was performed using:

* **Tokenizer:** `microsoft/phi-3-mini-4k-instruct`

### Token Statistics:

* **Maximum tokens:** < 2048
* **Average tokens:** ~50
* **Minimum tokens:** ~30

Samples exceeding the maximum context length were removed to ensure compatibility with fine-tuning.

A token-length histogram was generated to visualize distribution and identify outliers.

---

## 9. Train / Validation Split

The final dataset was split as follows:

* **Training set:** 90%
* **Validation set:** 10%

This ensures sufficient data for learning while allowing evaluation of generalization.

---

## 10. Suitability for Fine-Tuning

This dataset is well-suited for:

* LoRA / QLoRA fine-tuning
* Low-resource training environments (Colab)
* Quantized model training (4-bit / 8-bit)
* Instruction-following behavior improvement

---
