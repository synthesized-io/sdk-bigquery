#!/bin/bash

PLATFORM="linux/amd64"

# Define the Docker image name (passed as the first argument)
DOCKER_IMAGE_NAME="$1"

# Define the Docker Hub image metadata JSON (passed as the second argument)
DOCKER_METADATA_JSON="$2"

# Parse the JSON to extract tags
tags=$(echo "$DOCKER_METADATA_JSON" | jq -r '.tags | join(" ")')
IFS=' ' read -ra tags_array <<< "$tags"

docker pull "$DOCKER_IMAGE_NAME" --platform $PLATFORM

for tag in "${tags_array[@]}"; do
  export docker_tag_cmd="docker tag $DOCKER_IMAGE_NAME $tag"
  echo "$docker_tag_cmd"
  eval "$docker_tag_cmd"

  export docker_push_cmd="docker push $tag"
  echo "$docker_push_cmd"
  eval "$docker_push_cmd"
done
