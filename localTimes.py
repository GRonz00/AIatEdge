from vllm import LLM
prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]
llm = LLM(model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
          gpu_memory_utilization=0.85,
          max_model_len=4096,
          max_num_seqs=2,
          max_num_batched_tokens=4096,
          swap_space=2,
          enable_prefix_caching=True,
        )
outputs = llm.generate(prompts)
f = open("output.txt","w")
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    f.write(f"Prompt: {prompt!r}, Generated text: {generated_text!r}\n")
f.close()