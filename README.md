# Title Belt App

FastAPI service for NHL title belt app (see [title-belt-nhl](github.com/kawa2287/title-belt-nhl)).

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

