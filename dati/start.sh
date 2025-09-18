#!/usr/bin/env bash

# $! project id

set -euo pipefail

pushd terraform
terraform apply --auto-approve -var="project=$1"
popd
#gcloud compute config-ssh
#gcloud compute ssh vllm-instance
#source .venv/bin/activate
#export HF_TOKEN=

#gcloud compute scp install.sh vllm-instance:~
#gcloud compute scp prompts.json vllm-instance:~/project

 #python -m vllm.entrypoints.openai.api_server  --model google/gemma-3n-e2b-it     --port 8000     --host 127.0.0.1     --dtype bfloat16
#locust -f flusso.py    --host http://localhost:8000    --users 25    --spawn-rate 25    --run-time 5m    --headless --csv=report --csv-full-history
#curl http://0.0.0.0:8000/metrics -o gemma.txt