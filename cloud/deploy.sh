#!/bin/bash
set -e
set -u

# Set up environment variables:
export VPC_CONNECTOR=synthesized-connector
export BQ_CONNECTION_NAME="ext-synthesized-connection"

# Enable APIs for GCP services:
gcloud services enable \
  compute.googleapis.com \
  deploymentmanager.googleapis.com \
  iam.googleapis.com \
  bigquery.googleapis.com \
  bigqueryconnection.googleapis.com \
  vpcaccess.googleapis.com

# Create VPC connector to be able call service inside the GKE:
gcloud compute networks vpc-access connectors create $VPC_CONNECTOR \
   --region=$REGION \
   --network=$NETWORK \
   --range=$VPC_CONNECTOR_RANGE \
   --machine-type=f1-micro \
   --min-instances 2 \
   --max-instances 3

# Create GCP cloud functions:
gcloud deployment-manager deployments create synthesized-deployment --template=cloud-functions.jinja \
  --properties region:$REGION,vpcConnector:$VPC_CONNECTOR,clusterIP:$CLUSTER_IP

# Create BigQuery connection to call remote cloud functions:
bq mk --connection \
  --display_name='Synthesized external transform function connection' \
  --connection_type=CLOUD_RESOURCE \
  --project_id="${PROJECT}" \
  --location="${REGION}" \
  "${BQ_CONNECTION_NAME}"

# Get connection's Service Account:
CONNECTION_SA=$(bq --project_id ${PROJECT} --format json show --connection ${PROJECT}.${REGION}.${BQ_CONNECTION_NAME} | jq -r '.cloudResource.serviceAccountId')
# Get connection's Service Account:
gcloud projects add-iam-policy-binding ${PROJECT} \
  --member="serviceAccount:${CONNECTION_SA}" \
  --role='roles/run.invoker'

# Create BigQuery UDF to run Synthesized Task:
bq query --project_id ${PROJECT} \
  --use_legacy_sql=false \
  "CREATE OR REPLACE FUNCTION ${BQ_FUNCTION_DATASET}.synthesize(input_table STRING, output_table STRING, config STRING)
  RETURNS JSON
  REMOTE WITH CONNECTION \`${PROJECT}.${REGION}.${BQ_CONNECTION_NAME}\`
  OPTIONS (endpoint = 'https://${REGION}-${PROJECT}.cloudfunctions.net/synthesize-run');"

# Create BigQuery UDF to run check Synthesized Task state:
bq query --project_id ${PROJECT} \
  --use_legacy_sql=false \
  "CREATE OR REPLACE FUNCTION ${BQ_FUNCTION_DATASET}.check_synthesized(task_id STRING)
  RETURNS JSON
  REMOTE WITH CONNECTION \`${PROJECT}.${REGION}.${BQ_CONNECTION_NAME}\`
  OPTIONS (endpoint = 'https://${REGION}-${PROJECT}.cloudfunctions.net/synthesize-check');"
