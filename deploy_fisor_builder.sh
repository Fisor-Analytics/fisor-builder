# Set variables
RESOURCE_GROUP="fisor-api-rg"
ENV_NAME="fisor-env"
LOCATION="canadacentral"
APP_NAME="fisor-builder"
REGISTRY_NAME="fisorbuilderregistry"
IMAGE_NAME="${REGISTRY_NAME}.azurecr.io/fisor-builder:latest"

# 1. Create Container Apps environment (only once)
az containerapp env create \
  --name $ENV_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# 2. Deploy the app
az containerapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENV_NAME \
  --image $IMAGE_NAME \
  --target-port 8000 \
  --ingress external \
  --registry-server ${REGISTRY_NAME}.azurecr.io \
  --query configuration.ingress.fqdn \
  --cpu 0.5 --memory 1.0Gi \
  --transport auto

