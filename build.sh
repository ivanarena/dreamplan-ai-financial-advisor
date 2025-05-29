#!/usr/bin/env bash
set -euo pipefail

export $(grep -v '^#' .env | xargs)

docker buildx build \
    --secret id=OPENAI_API_KEY,src=<(echo -n "$OPENAI_API_KEY") \
    --secret id=CALCULATION_API_URL,src=<(echo -n "$CALCULATION_API_URL") \
    -t dreamplan-ai \
    .