#google/gemma-3n-e2b-it
#Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4
import json, time, csv, threading
import pynvml
from vllm import LLM, SamplingParams
pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)
def monitor_gpu(stop_flag, interval=0.2):
    samples = []
    while not stop_flag["stop"]:
        power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000  # in Watt
        util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        mem = pynvml.nvmlDeviceGetMemoryInfo(handle).used / 1024 / 1024
        timestamp = time.time()
        samples.append((timestamp, power, util, mem))
        time.sleep(interval)
    return samples
def run(model):
    N = 200 #numero di prompt da usare
    questions = []
    with open("prompts.json", 'r') as f:
        for i, line in enumerate(f):
            if i >= N:
                break
            item = json.loads(line)
            questions.append(item['question'])


    llm = LLM(model=model,
              task="generate",
              gpu_memory_utilization=0.85,
              max_model_len=4096,
              max_num_seqs=2,
              max_num_batched_tokens=4096,
              swap_space=2,
              enable_prefix_caching=True,
            )
    with open(model.split('/')[0]+".csv", "w") as f:
        writer = csv.writer(f)
        #writer.writerow(["question", "answer", "clock_time", "total_latency", "ttft","token_prompt","token_out"])
        writer.writerow(["question", "answer", "clock_time", "total_latency", "ttft",
                         "token_prompt", "token_out", "avg_power_W", "avg_util_%", "avg_mem_MB", "energy_kWh"])
        s = SamplingParams(max_tokens=2048)
        for q in questions:
            stop_flag = {"stop": False}
            gpu_samples = []
            def monitor():
                nonlocal gpu_samples
                gpu_samples = monitor_gpu(stop_flag)
            monitor_thread = threading.Thread(target=monitor)
            monitor_thread.start()

            start = time.time()
            output = llm.generate([q],sampling_params=s)[0]
            end = time.time()

            stop_flag["stop"] = True
            monitor_thread.join()
            if gpu_samples:
                powers = [x[1] for x in gpu_samples]
                utils = [x[2] for x in gpu_samples]
                mems  = [x[3] for x in gpu_samples]
                avg_power = sum(powers) / len(powers)
                avg_util = sum(utils) / len(utils)
                avg_mem = sum(mems) / len(mems)
                clock_time = end - start
                energy_kWh = (avg_power * clock_time) / 3600000  # Joule → kWh
            else:
                avg_power = avg_util = avg_mem = energy_kWh = None
                clock_time = end - start
            generated_text = output.outputs[0].text.strip().replace("\n", " ")
            metrics = output.metrics
            if metrics and metrics.finished_time and metrics.arrival_time:
                total_latency = metrics.finished_time - metrics.arrival_time
            else:
                total_latency = None

            ttft = metrics.first_token_time if metrics and metrics.first_token_time else None

            #writer.writerow([q, generated_text, end - start, total_latency, ttft,len(output.prompt_token_ids),len(output.outputs[0].token_ids)])
            writer.writerow([q, generated_text, clock_time, total_latency, ttft,
                             len(output.prompt_token_ids), len(output.outputs[0].token_ids),
                             avg_power, avg_util, avg_mem, energy_kWh])

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python localTimes.py <model_name>")
        sys.exit(1)
    model_name = sys.argv[1]
    run(model_name)
    input("inv per terminare")