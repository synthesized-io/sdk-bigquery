# Cloud resources installation

## Prerequisites

### Setting up command-line tools

You need the following tools in your development environment:

- [gcloud](https://cloud.google.com/sdk/gcloud/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Enable APIs for GCP services:

```shell
gcloud services enable \
    compute.googleapis.com \
    deploymentmanager.googleapis.com \
    iam.googleapis.com \
    bigquery.googleapis.com \
    bigqueryconnection.googleapis.com \
    vpcaccess.googleapis.com
```

### Configure installation parameters

> **_NOTE:_**  The values in the code blocks are just examples. Please change values if necessary here and below.

```shell
export APP_INSTANCE_NAME=synthesized-sdk
export NAMESPACE=synthesized-sdk
```

Set VPC network, the list: https://console.cloud.google.com/networking/networks/list:
```shell
export NETWORK=default
```

Set GCP project ID and region. Please change the values to needed:
```shell
export REGION=us-west1
export PROJECT=[My Project]
```

Set external IP address of your Flower Web Server, deployed in the GKE cluster:

```shell
export CLUSTER_IP="$(kubectl get "service/${APP_INSTANCE_NAME}-flower-service" \
    --namespace "${NAMESPACE}" \
    --output jsonpath='{.status.loadBalancer.ingress[0].ip}')"
```

Configure IP range for VPC connector to access GKE cluster from Cloud Functions.
Please read https://cloud.google.com/vpc/docs/serverless-vpc-access for details.
```shell
export VPC_CONNECTOR_RANGE=10.8.0.0/28
```

Set BigQuery dataset where to use SDK:
```shell
export BQ_FUNCTION_DATASET=dataset
```

### Run installation script

Run the deployment script:
```shell
cd cloud
./deploy.sh
```

If necessary, the commands can be executed one after another in the correct order.
