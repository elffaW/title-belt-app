# Title Belt App

FastAPI service and website for NHL title belt app (see [title-belt-nhl](github.com/kawa2287/title-belt-nhl)).

## Where??

https://title-belt-app.onrender.com/
`/docs` for swagger docs

## How??

https://docs.render.com/deploy-fastapi
- Deployment uses Python 3.11, Poetry 1.7

```
poetry install --no-root
```

```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Why??

So we can do a cool website that shows us the belt holder and stuff.


## Deploy??

### Render

### GCP

#### Cloud Run

Deploys an app from a docker image, which we need to build (from `Dockerfile`) and push to a registry (we use GCP Artifact Registry).

* Auth
```sh
gcloud auth configure-docker us-east1-docker.pkg.dev  # (one time) 
gcloud auth login --update-adc  # expires periodically (24 hours?)
gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin https://us-east1-docker.pkg.dev
```
* Push docker image
```
docker push <image>
```
* Deploy app
```
gcloud run deploy title-belt-app --image <image>
```
