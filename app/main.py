from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from title_belt_nhl.schedule import Schedule

from app import templates
from app import api
from app.models import NhlTeams

app = FastAPI()

app.include_router(api.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


def _build_full_page_context(request: Request):
    teams = [t.value for t in NhlTeams]
    selected_team = ""
    schedule = Schedule("")
    holder = schedule.belt_holder

    return {
        "request": request,
        "belt_holder": holder,
        "numGames": "",
        "path": "",
        "teams": teams,
        "team": selected_team,
        "season": schedule.season,
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
