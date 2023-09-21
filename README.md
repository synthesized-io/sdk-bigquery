# Overview

Synthesized Scientific Data Kit (SDK) is a comprehensive framework for generative modelling for structured data (tabular, time-series and event-based data). The SDK helps you create compliant statistical-preserving data snapshots for BI/Analytics and ML/AI applications. Right-size your data with AI-supported data transformations.

Available on the GCP Cloud Marketplace: https://console.cloud.google.com/marketplace/product/synthesized-marketplace-public/synthesized-sdk

# Architecture

![architecture.png](docs%2Fimages%2Farchitecture.png)

# Installation

![deployment.png](docs%2Fimages%2Fdeployment.png)

## Deploy Kubernetes resources

### Quick install with Google Cloud Marketplace

To install Synthesized SDK Service to a Google Kubernetes Engine cluster via Google Cloud Marketplace, follow the
[on-screen instructions](https://console.cloud.google.com/marketplace/product/synthesized-marketplace-public/synthesized-sdk).

### Command-line instructions

[Kubernetes CLI installation](docs%2Fk8s-cli-installation.md)

### Viewing your app in the Google Cloud Console

To get the Cloud Console URL for your app, run the following command:

```shell
echo "https://console.cloud.google.com/kubernetes/application/${ZONE}/${CLUSTER}/${NAMESPACE}/${APP_INSTANCE_NAME}"
```

To view the app, open the URL in your browser.

## Deploy cloud resources

[Cloud resources installation](docs%2Fcloud-resources-installation.md)

# Using the app

## How to use SDK service

Navigate to [BigQuery](https://console.cloud.google.com/bigquery) and make sure that `synthesize` and `check_synthesized` 
routines exist under the specified dataset.

The created functions look like this:

![bigquery_functions.png](docs%2Fimages%2Fbigquery_functions.png)

Change the dataset, table names and [config](https://docs.synthesized.io/sdk/latest/getting_started/yaml) and run the following SQL script:
```sql
SELECT dataset.synthesize('input_table', 'output_table', '{"synthesize": {"num_rows": 1000, "produce_nans": true}}');
```

The output should be similar to
```json
{"status":"success","task_id":"d15d63f5-d476-47e2-814f-f8323ca844fb"}
```

You can check the status of the task with the following script:
```sql
SELECT dataset.check_synthesized('d15d63f5-d476-47e2-814f-f8323ca844fb');
```

# Scaling

The number of SDK Celery workers can be increased with the property `worker.replicas`.

# App metrics

At the moment, the application does not support exporting Prometheus metrics and does not have any exporter.

# Uninstalling the app

## Delete Kubernetes resources

### Using the Google Cloud Console

1.  In the Cloud Console, open
    [Kubernetes Applications](https://console.cloud.google.com/kubernetes/application).

2.  From the list of apps, choose your app installation.

3.  On the **Application Details** page, click **Delete**.

### Using the command-line

#### Preparing your environment

Set your installation name and Kubernetes namespace:

```shell
export APP_INSTANCE_NAME=sdk-service
export NAMESPACE=default
```

#### Deleting your resources

> **NOTE:** We recommend using a `kubectl` version that is the same as the
> version of your cluster. Using the same version for `kubectl` and the cluster
> helps to avoid unforeseen issues.

##### Deleting the deployment with the generated manifest file

Run `kubectl` on the expanded manifest file:

```shell
kubectl delete -f ${APP_INSTANCE_NAME}_manifest.yaml --namespace ${NAMESPACE}
```

##### Deleting the deployment by deleting the Application resource

If you don't have the expanded manifest file, delete the resources by using
types and a label:

```shell
kubectl delete application,deployment,secret,service,statefulset \
  --namespace ${NAMESPACE} \
  --selector name=${APP_INSTANCE_NAME}
```

## Delete cloud resources

Set GCP project ID and region. Please change the values to needed:
```shell
export REGION=us-west1
```

Set BigQuery dataset:
```shell
export BQ_FUNCTION_DATASET=dataset
```

Run the script and confirm deletion:
```shell
./cloud/clean.sh
```
