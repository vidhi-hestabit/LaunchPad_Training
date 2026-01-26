# Instruction Tuning Dataset – HR Domain

## Dataset Overview
- Domain: HR QA
- Total samples: 568
- Format: Instruction-style JSONL
- Split:
  - Train: 90% (358)
  - Validation: 10% (40)

## Sample Types
Each base QA pair was expanded into three instruction types:

1. **QA**
   - Direct HR question answering
2. **Reasoning**
   - Step-by-step HR reasoning with conclusion
3. **Extraction**
   - Structured information extraction from HR

Distribution is balanced across all three types.

## Data Cleaning
- Renamed columns to `input` / `output`
- Removed null rows
- Removed duplicate question–answer pairs
- Filtered samples by token length

## Token Length Filtering
- Minimum tokens: 10
- Maximum tokens: 512
- Tokenizer: Mistral-7B (SentencePiece, fast tokenizer)

A token length histogram was generated to identify and remove outliers.

## Instruction Format
Each sample follows:

```json
{
  "instruction": "...",
  "input": "...",
  "output": "..."
}
```