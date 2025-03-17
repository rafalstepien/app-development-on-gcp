# simple-oauth-app
This is a first try to implement an API secured with OAuth 2.0 token with Google as IdP.

> **Note**
> 
> `client_secrets.json` file should be downloaded from Google Cloud Platform (OAuth consent screen -> clients) and named exactly like this

## Commands for gcloud CLI
### Set region and application name
```
REGION=europe-central2
APP=api-oauth
```
### Create an Artifact Registry to store Docker images
```
gcloud artifacts repositories create ${APP} --location=${REGION} --repository-format=docker
```

### Build and push app image to Artifact Registry
```
docker build -t ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/${APP}/api:1.0 .
docker push ${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/${APP}/api:1.0
```
### Deploy image on Cloud Run
```
gcloud run deploy ${APP} \
    --image=${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/${APP}/api:1.0 \
    --allow-unauthenticated \
    --region=${REGION}
```
> **Note**: We allow unauthenticated traffic to the service, because endpoints are secured and require passing
> an ID token anyway.