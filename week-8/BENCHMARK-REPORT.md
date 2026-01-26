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
GGUF Q8 llama.cpp	3.54	    99.41	        0.0	       0.901
Base Model	        54.39	    7.87        5050.44	        0.86
Fine-tuned	        55.54	    7.71	    5050.44	        0.86


<hr>

---

Below are the results produced when inferencing was performed on colab using T4 GPU with streaming on :
Model	            Tokens/sec	        Latency (s)	        VRAM (MB)	    Accuracy
GGUF Q8 llama.cpp	3.88	            4.13	            2530.31	        0.722
Base Model	        194.55	            0.17	            6726.91	        0.777
Fine-tuned	        197.53	            0.17	            6726.91	        0.777