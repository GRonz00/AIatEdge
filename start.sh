#!/usr/bin/env bash

# $! project id

set -euo pipefail

pushd terraform
terraform apply --auto-approve -var="project=$1"
popd
#gcloud compute config-ssh
#gcloud compute scp install.sh vllm-instance:~
#gcloud compute ssh vllm-instance