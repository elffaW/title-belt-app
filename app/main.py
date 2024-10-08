from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from title_belt_nhl.schedule import Schedule

from app import templates
from app import api
from app.models import NhlTeams

app = FastAPI()

app.include_router(api.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


def _build_full_page_context(request: Request):
    teams = [t for t in NhlTeams]
    schedule = Schedule("")
    holder = schedule.belt_holder
    selected_team = holder

    return {
        "request": request,
        "belt_holder": NhlTeams[holder].value,
        "numGames": -1,
        "teams": teams,
        "team": selected_team,
        "season": schedule.get_season_pretty(),
        "schedule": [],
    }


@app.get("/")
async def root(request: Request):
    context = _build_full_page_context(request)
    return templates.TemplateResponse("home.html", context)

@app.get("/heartbeat")
def heartbeat():
    return {"message": "Success!"}
