#!/usr/bin/env bash

# $! project id

set -euo pipefail

pushd terraform
terraform apply --var="project=$1"

gcloud compute scp install.sh vllm-instance:~
popd

gcloud compute ssh vllm-instance