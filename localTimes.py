#"deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
import json
import time
import csv
from vllm import LLM, SamplingParams
N = 100 #numero di prompt da usare
questions = []
with open("nq-dev-sample.json", 'r') as f:
    for i, line in enumerate(f):
        if i >= N:
            break
        item = json.loads(line)
        questions.append(item['question'])


llm = LLM(model="Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4",
          task="generate",
          gpu_memory_utilization=0.85,
          max_model_len=4096,
          max_num_seqs=2,
          max_num_batched_tokens=4096,
          swap_space=2,
          enable_prefix_caching=True,
        )
with open("output.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["question", "answer", "clock_time", "total_latency", "ttft","token_prompt","token_out"])
    for q in questions:
        start = time.time()
        s = SamplingParams(max_tokens=128)
        output = llm.generate([q],sampling_params=s)[0]
        end = time.time()
        prompt = output.prompt
        generated_text = output.outputs[0].text.strip().replace("\n", " ")
        metrics = output.metrics
        if metrics and metrics.finished_time and metrics.arrival_time:
            total_latency = metrics.finished_time - metrics.arrival_time
        else:
            total_latency = None

        ttft = metrics.first_token_time if metrics and metrics.first_token_time else None

        writer.writerow([q, generated_text, end - start, total_latency, ttft,len(output.prompt_token_ids),len(output.outputs[0].token_ids)])