# Training Report

## **Model Overview**
We fine-tuned a pre-trained language model, **TinyLlama/TinyLlama-1.1B-Chat-v1.0**, using **Parameter-Efficient Fine-Tuning (PEFT)**, specifically with **LoRA** (Low-Rank Adaptation) techniques. The objective of this fine-tuning was to create an efficient model while using memory-saving tricks such as 4-bit quantization and gradient checkpointing.

### **Key Points:**
- **LoRA (QLoRA)**: LoRA is applied to fine-tune the model with only a small number of trainable parameters, drastically reducing the computational burden during fine-tuning.
- **4-bit Quantization**: Model weights are loaded in 4-bit precision using the `BitsAndBytes` library, reducing the memory footprint while maintaining performance.
- **Gradient Checkpointing**: This technique is enabled to save memory during training by storing only certain layers of the model in memory at each step.

---

## **Training Setup**
### **Model and Tokenizer**
- **Model Name**: `TinyLlama/TinyLlama-1.1B-Chat-v1.0`
- **Tokenizer**: Hugging Face `AutoTokenizer` is used, with padding and EOS token adjustments.
- **Quantization**: `BitsAndBytes` is configured for 4-bit quantization, and `bnb_4bit_quant_type="nf4"` is chosen for lower precision quantization.

### **Training Hyperparameters**
- **Learning Rate (LR)**: `2e-4`
- **Batch Size**: `4`
- **Epochs**: `3`
- **Maximum Sequence Length**: `512`
- **Gradient Accumulation Steps**: `2`
- **Weight Optimizer**: `paged_adamw_8bit`
- **Precision**: Mixed precision (FP16=False, BF16=True)
- **Warmup Ratio**: `0.05`
- **Max Gradient Norm**: `1.0`
- **Optimizer**: Paged AdamW with 8-bit precision

---

## **LoRA Configuration**
- **Rank (r)**: `16`
- **Alpha**: `32`
- **Dropout**: `0.05`
- **Target Modules**: `"q_proj", "v_proj"` 

---

## **Dataset**
- **Train Data**: `/content/train.jsonl`
- **Validation Data**: `/content/val.jsonl`
- **Formatting Function**: We used a specific formatting function to convert the data into the desired input-output structure for the model, which includes:
  - Instruction
  - Input
  - Output

---

## **Training Process**
The model was fine-tuned using the **SFTTrainer** (Supervised Fine-Tuning Trainer) from the **TRL** library, which streamlines the fine-tuning of models for causal language modeling tasks.

- The **Data Collator** used was `DataCollatorForLanguageModeling` with `mlm=False`, as we are performing causal language modeling.
- **Training Execution**:
  - The training process is carried out using gradient accumulation to ensure we stay within memory constraints.
  - LoRA adapters are applied, and the model is updated with minimal trainable parameters (approximately 1% of the total model size).

---

## **Model Evaluation**
### **Test Prompt**:

### Instruction:
Analyze the HR scenario step by step, clearly explain the HR reasoning, and conclude.

### Input:
What are stay bonuses and when are they used?

### **Response**:

### Response:
---

Stay bonuses are incentives for employees who remain with an organization beyond a certain length of time (usually 12 months). They can be paid as cash or as additional compensation such as stock options or promotions. When to use them depends on organizational goals, employee performance, and company culture. For example, if the goal is retention rather than productivity gains, longer-term stays may be more valuable. If there's high turnover due to benefits packages that don't align with needs, shorter stays might be better. In some cases, companies have policies requiring at least three

---

### Total Loss :

![alt text](<Screenshot from 2026-01-26 14-25-50.png>)