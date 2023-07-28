# Overview

Synthesized Scientific Data Kit (SDK) is a comprehensive framework for generative modelling for structured data (tabular, time-series and event-based data). The SDK helps you create compliant statistical-preserving data snapshots for BI/Analytics and ML/AI applications. Right-size your data with AI-supported data transformations.

Available on the GCP Cloud Marketplace: https://console.cloud.google.com/marketplace/product/synthesized-marketplace-public/synthesized-sdk-service

# Architecture

//TODO

# Installation

## Quick install with Google Cloud Marketplace

To install Synthesized SDK Service to a Google Kubernetes Engine cluster via Google Cloud Marketplace, follow the
[on-screen instructions](https://console.cloud.google.com/marketplace/product/synthesized-marketplace-public/synthesized-sdk-service).

## Command-line instructions

### Prerequisites

#### Setting up command-line tools

You need the following tools in your development environment:

- [gcloud](https://cloud.google.com/sdk/gcloud/)
- [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/)
- [Docker](https://docs.docker.com/install/)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Helm](https://helm.sh/)

Configure `gcloud` as a Docker credential helper:

```shell
gcloud auth configure-docker
```

#### Creating a Google Kubernetes Engine (GKE) cluster

Create a new cluster from the command line:

```shell
export CLUSTER=sdk-cluster
export ZONE=us-west1-a

gcloud container clusters create "${CLUSTER}" --zone "${ZONE}"
```

Configure `kubectl` to connect to the new cluster:

```shell
gcloud container clusters get-credentials "${CLUSTER}" --zone "${ZONE}"
```

#### Cloning this repo

Clone this repo, as well as its associated tools repo:

```shell
git clone --recursive https://github.com/synthesized-io/sdk-bigquery.git
```

#### Installing the Application resource definition

An Application resource is a collection of individual Kubernetes
components, such as Services, Deployments, and so on, that you can
manage as a group.

To set up your cluster to understand Application resources, run the
following command:

```shell
kubectl apply -f "https://raw.githubusercontent.com/GoogleCloudPlatform/marketplace-k8s-app-tools/master/crd/app-crd.yaml"
```

You need to run this command once.

The Application resource is defined by the
[Kubernetes SIG-apps](https://github.com/kubernetes/community/tree/master/sig-apps)
community. You can find the source code at
[github.com/kubernetes-sigs/application](https://github.com/kubernetes-sigs/application).

### Installing the app

#### Configuring the app with environment variables

Choose an instance name and
[namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
for the app. In most cases, you can use the `default` namespace.

```shell
export APP_INSTANCE_NAME=sdk-service
export NAMESPACE=default
```

Set up the image tag.
Example:

```shell
export TAG="2.7.0"
```

Configure the container images:

```shell
export IMAGE_REGISTRY="gcr.io/synthesized-marketplace-public/sdk-service"

export IMAGE_FLOWER="${IMAGE_REGISTRY}/flower"
export IMAGE_REDIS="${IMAGE_REGISTRY}/redis"
export IMAGE_WORKER="${IMAGE_REGISTRY}/worker"
```

(Optional) Set computation resources limit:

```shell
export FLOWER_RESOURCES_LIMITS_CPU=0.5
export FLOWER_RESOURCES_LIMITS_MEMORY=512Mi

export REDIS_DISK_SIZE_GB=1Gi

export WORKER_REPLICAS=1
export WORKER_RESOURCES_LIMITS_CPU=0.5
export WORKER_RESOURCES_LIMITS_MEMORY=512Mi
```

If you use a different namespace than the `default`, create a new namespace by
running the following command:

```shell
kubectl create namespace "${NAMESPACE}"
```

#### Creating the Service Account

To create the Service Account and ClusterRoleBinding:

```shell
export SDK_SERVICE_ACCOUNT="${APP_INSTANCE_NAME}-serviceaccount"
kubectl create serviceaccount "${SDK_SERVICE_ACCOUNT}" --namespace "${NAMESPACE}"
kubectl create clusterrole "${SDK_SERVICE_ACCOUNT}-role" --verb=get,list,watch --resource=services,nodes,pods,namespaces
kubectl create clusterrolebinding "${SDK_SERVICE_ACCOUNT}-rule" --clusterrole="${SDK_SERVICE_ACCOUNT}-role" --serviceaccount="${NAMESPACE}:${SDK_SERVICE_ACCOUNT}"
```

Set or generate the password for the GitLab services:

```shell
# Generate password for Redis
export REDIS_ROOT_PASSWORD="$(openssl rand -base64 12)"
```

For persistent disk provisioning of the GitLab StatefulSets, you will need to
specify the StorageClass name, or create a new StorageClass.

To check your available options, use the following command:

```shell
kubectl get storageclass
```

For steps to create a new StorageClass, refer to the
[Kubernetes documentation](https://kubernetes.io/docs/concepts/storage/storage-classes/#the-storageclass-resource)

```shell
export REDIS_STORAGE_CLASS="standard" # provide your StorageClass name if not "standard"
```

#### Expanding the manifest template

Use `helm template` to expand the template. We recommend that you save the
expanded manifest file for future updates to your app.

```shell
helm template chart/sdk-service \
  --name-template "${APP_INSTANCE_NAME}" \
  --namespace "${NAMESPACE}" \
  --set serviceAccount="${SDK_SERVICE_ACCOUNT}" \
  --set flower.image.repository="${IMAGE_FLOWER}" \
  --set flower.image.tag="${TAG}" \
  --set redis.image.repository="${IMAGE_REDIS}" \
  --set redis.image.tag="${TAG}" \
  --set worker.image.repository="${IMAGE_WORKER}" \
  --set worker.image.tag="${TAG}" \
  --set redis.password="${REDIS_ROOT_PASSWORD}" \
  --set redis.persistence.storageClass="${REDIS_STORAGE_CLASS}" \
  --set redis.persistence.size="${REDIS_PERSISTENCE_SIZE_GB}" \
  --set worker.replicas="${WORKER_REPLICAS}" \
  --set flower.resources.limits.cpu="${FLOWER_RESOURCES_LIMITS_CPU}" \
  --set flower.resources.limits.memory="${FLOWER_RESOURCES_LIMITS_MEMORY}" \
  --set worker.resources.limits.cpu="${WORKER_RESOURCES_LIMITS_CPU}" \
  --set worker.resources.limits.memory="${WORKER_RESOURCES_LIMITS_MEMORY}" \
  > "${APP_INSTANCE_NAME}_manifest.yaml"
```

#### Applying the manifest to your Kubernetes cluster

To apply the manifest to your Kubernetes cluster, use `kubectl`:

```shell
kubectl apply -f "${APP_INSTANCE_NAME}_manifest.yaml" --namespace "${NAMESPACE}"
```

#### Viewing your app in the Google Cloud Console

To get the Cloud Console URL for your app, run the following command:

```shell
echo "https://console.cloud.google.com/kubernetes/application/${ZONE}/${CLUSTER}/${NAMESPACE}/${APP_INSTANCE_NAME}"
```

To view the app, open the URL in your browser.

### Accessing the Flower User Interface

You can expose Flower Web Server port:

```shell
kubectl port-forward \
    --namespace "${NAMESPACE}" \
    svc/${APP_INSTANCE_NAME}-flower-service \
    5555:5555
```

# Using the app

## How to use SDK service

//TODO

# Scaling

The number of SDK Celery workers can be increased with the Helm Chart property `worker.replicas`.

# App metrics

At the moment, the application does not support exporting Prometheus metrics and does not have any exporter.

# Uninstalling the app

## Using the Google Cloud Console

1.  In the Cloud Console, open
    [Kubernetes Applications](https://console.cloud.google.com/kubernetes/application).

2.  From the list of apps, choose your app installation.

3.  On the **Application Details** page, click **Delete**.

## Using the command-line

### Preparing your environment

Set your installation name and Kubernetes namespace:

```shell
export APP_INSTANCE_NAME=sdk-service
export NAMESPACE=default
```

### Deleting your resources

> **NOTE:** We recommend using a `kubectl` version that is the same as the
> version of your cluster. Using the same version for `kubectl` and the cluster
> helps to avoid unforeseen issues.

#### Deleting the deployment with the generated manifest file

Run `kubectl` on the expanded manifest file:

```shell
kubectl delete -f ${APP_INSTANCE_NAME}_manifest.yaml --namespace ${NAMESPACE}
```

#### Deleting the deployment by deleting the Application resource

If you don't have the expanded manifest file, delete the resources by using
types and a label:

```shell
kubectl delete application,deployment,secret,service,statefulset,backendconfig \
  --namespace ${NAMESPACE} \
  --selector name=${APP_INSTANCE_NAME}
```
