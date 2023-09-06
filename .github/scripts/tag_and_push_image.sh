#!/bin/bash

# Define the Docker image name (passed as the first argument)
DOCKER_IMAGE_NAME="$1"

# Define the Docker Hub image metadata JSON (passed as the second argument)
DOCKER_METADATA_JSON="$2"

# Parse the JSON to extract tags
tags=$(echo "$DOCKER_METADATA_JSON" | jq -r '.tags | join(" ")')
IFS=' ' read -ra tags_array <<< "$tags"

# Build the docker command
docker_cmd="docker buildx imagetools create"
for tag in "${tags_array[@]}"; do
  docker_cmd+=" --tag $tag"
done

# Append the image name
docker_cmd+=" $DOCKER_IMAGE_NAME"

# Print the command for debugging purposes
echo "$docker_cmd"

# Execute the docker command
eval "$docker_cmd"
