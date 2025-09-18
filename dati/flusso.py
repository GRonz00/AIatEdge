import json
import random
from locust import HttpUser, task, constant_pacing

def load_prompts(file_path="prompts.json"):
    questions = []
    with open(file_path, 'r') as f:
        for _, line in enumerate(f):
            item = json.loads(line)
            questions.append(item['question'])
    return questions

class VLLMLoadTest(HttpUser):
    # Ogni utente invia una richiesta ogni 2 secondi, indipendentemente dalla latenza
    wait_time = constant_pacing(0.1)

    # Endpoint API compatibile con OpenAI
    endpoint = "/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    prompts = load_prompts()

    @task
    def send_request(self):
        # Ogni utente prende un prompt casuale
        prompt = random.choice(self.prompts)

        data = {
            "model": "google/gemma-3n-e2b-it",  # Sostituisci col modello vLLM
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        # Invio richiesta POST
        with self.client.post(self.endpoint, data=json.dumps(data), headers=self.headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Errore {response.status_code}: {response.text}")
