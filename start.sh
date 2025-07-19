#!/usr/bin/env bash

# $! project id

set -euo pipefail

terraform apply --var="project=$1"

gcloud compute scp install.sh vllm-instance:~
gcloud compute ssh vllm-instance "bash install.sh"
gcloud compute ssh vllm-instance