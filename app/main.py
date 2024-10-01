from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles

from app import templates
from app import api

app = FastAPI()

app.include_router(api.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


def _build_full_page_context(request: Request):
  teams = []
  selected_team = ""

  return {
    "request": request,
    "teams": teams,
    "selected_team": selected_team
  }


# def _get_reminders_grid(request: Request):
#   context = _build_full_page_context(request)
#   return templates.TemplateResponse("partials/reminders/content.html", context)


@app.get("/")
async def root(request: Request):
    context = _build_full_page_context(request)
    return templates.TemplateResponse("home.html", context)

@app.get("/heartbeat")
def heartbeat():
    return {"message": "Success!"}
