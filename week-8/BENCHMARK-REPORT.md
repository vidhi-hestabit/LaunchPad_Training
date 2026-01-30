# Benchmark Report

## Models Tested
- Base TinyLlama 1.1B Chat
- Fine-tuned LoRA merged
- GGUF Q8 (llama.cpp)

## Metrics
- Tokens/sec
- Latency
- VRAM usage
- Accuracy (semantic similarity)

## Results Summary

Below are the results produced when inferencing was performed on Local Machine :

Model	            Tokens/sec	Latency (s)	VRAM (MB)	 Accuracy
GGUF Q8 llama.cpp	3.54	    99.41	        0.0	        0.83
Base Model	        54.39	    7.87        5050.44	        0.86
Fine-tuned	        55.54	    7.71	    5050.44	        0.90


<hr>

---

Below are the results produced when inferencing was performed on colab using T4 GPU with streaming on :
Model               Tokens/sec   TTFT (s)   VRAM (MB)   Accuracy
Base Model (FP16)      190        0.15      6710        0.77
Fine-tuned (LoRA)     185         0.16      6700        0.80
GGUF Q8 (CPU)          4           1        0           0.72
