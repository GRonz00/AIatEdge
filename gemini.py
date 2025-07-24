import json
import os
import time
import csv
from google import genai
from google.genai import types
def run(model="gemini-2.5-flash",thinking=False):
    N = 200 #numero di prompt da usare
    questions = []
    # Turn off thinking:
    t = types.ThinkingConfig(thinking_budget=0)
    if thinking:
        #thinking dinamico, il modello sceglio quando e quanto pensare
        t=types.ThinkingConfig(thinking_budget=-1)
    with open("nq-dev-sample.json", 'r') as f:
        for i, line in enumerate(f):
            if i >= N:
                break
            item = json.loads(line)
            questions.append(item['question'])
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    with open(f"{model}_{thinking}.csv","w") as f:
        writer = csv.writer(f)
        writer.writerow(["question", "answer", "clock_time","prompt_token","candidates_token","thoughtsTokenCount","totalTokenCount"])

        for q in questions:
            start = time.time()
            response = client.models.generate_content(
                model=model, contents=q,
                config=types.GenerateContentConfig(

                    thinking_config=t
                ),
            )
            end = time.time()
            answer = response.text.strip().replace("\n", " ")
            usage = response.usage_metadata
            writer.writerow([q, answer, end - start,usage.prompt_token_count,usage.candidates_token_count,usage.thoughtsTokenCount,usage.total_token_count])

if __name__ == "__main__":
    run("gemini-2.5-flash",False)
    run("gemini-2.5-flash",True)
    run("gemini-2.5-flash-lite",False)
    run("gemini-2.5-flash",True)