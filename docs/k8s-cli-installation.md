# Kubernetes resources installation

> **_NOTE:_**  The CLI installation is only available if you have successfully deployed SDK from the marketplace
> and reporting service key was generated.

## Prerequisites

### Setting up command-line tools

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

### Creating a Google Kubernetes Engine (GKE) cluster

Create a new cluster from the command line. Please note that the BigQuery scope is required.
You can change values of the properties CLUSTER and ZONE.

```shell
export CLUSTER=sdk-cluster
export ZONE=us-west1-a

gcloud container clusters create "${CLUSTER}" --zone "${ZONE}" --scopes=gke-default,bigquery
```

Configure `kubectl` to connect to the new cluster:

```shell
gcloud container clusters get-credentials "${CLUSTER}" --zone "${ZONE}"
```

### Cloning this repo

Clone this repo, as well as its associated tools repo:

```shell
git clone --recursive https://github.com/synthesized-io/sdk-bigquery.git
```

### Installing the Application resource definition

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

## Installing the app

### Configuring the app with environment variables

Choose an instance name and
[namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
for the app.

```shell
export APP_INSTANCE_NAME=synthesized-sdk
export NAMESPACE=synthesized-sdk
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

export REDIS_DISK_SIZE=128Mi

export WORKER_REPLICAS=1
export WORKER_RESOURCES_LIMITS_CPU=0.5
export WORKER_RESOURCES_LIMITS_MEMORY=512Mi
```

If you use a different namespace than the `default`, create a new namespace by
running the following command:

```shell
kubectl create namespace "${NAMESPACE}"
```

### Creating the Service Account

To create the Service Account and ClusterRoleBinding:

```shell
export SDK_SERVICE_ACCOUNT="${APP_INSTANCE_NAME}-serviceaccount"
kubectl create serviceaccount "${SDK_SERVICE_ACCOUNT}" --namespace "${NAMESPACE}"
kubectl create clusterrole "${SDK_SERVICE_ACCOUNT}-role" --verb=get,list,watch --resource=services,nodes,pods,namespaces
kubectl create clusterrolebinding "${SDK_SERVICE_ACCOUNT}-rule" --clusterrole="${SDK_SERVICE_ACCOUNT}-role" --serviceaccount="${NAMESPACE}:${SDK_SERVICE_ACCOUNT}"
```

Set or generate the password for Redis:

```shell
# Generate password for Redis
export REDIS_ROOT_PASSWORD="$(openssl rand -base64 12)"
```

For persistent disk provisioning of the Redis StatefulSet, you will need to
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

### Expanding the manifest template

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
  --set redis.persistence.size="${REDIS_DISK_SIZE}" \
  --set worker.replicas="${WORKER_REPLICAS}" \
  --set flower.resources.limits.cpu="${FLOWER_RESOURCES_LIMITS_CPU}" \
  --set flower.resources.limits.memory="${FLOWER_RESOURCES_LIMITS_MEMORY}" \
  --set worker.resources.limits.cpu="${WORKER_RESOURCES_LIMITS_CPU}" \
  --set worker.resources.limits.memory="${WORKER_RESOURCES_LIMITS_MEMORY}" \
  --set reportingSecret="${APP_INSTANCE_NAME}-reporting-secret" \
  > "${APP_INSTANCE_NAME}_manifest.yaml"
```

### Applying the manifest to your Kubernetes cluster

To apply the manifest to your Kubernetes cluster, use `kubectl`:

```shell
kubectl apply -f "${APP_INSTANCE_NAME}_manifest.yaml" --namespace "${NAMESPACE}"
```
