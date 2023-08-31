#!/bin/bash
set -e
set -u

# Set up environment variables:
export VPC_CONNECTOR=synthesized-connector
export BQ_CONNECTION_NAME="ext-synthesized-connection"

# Delete BigQuery UDFs and connection:
bq rm --routine --force ${BQ_FUNCTION_DATASET}.check_synthesized
bq rm --routine --force ${BQ_FUNCTION_DATASET}.synthesize
bq rm --connection --location="${REGION}" --force "${REGION}.${BQ_CONNECTION_NAME}"

# Delete Cloud Functions:
gcloud deployment-manager deployments delete synthesized-deployment

# Delete VPC connector:
gcloud compute networks vpc-access connectors delete $VPC_CONNECTOR --region="${REGION}"
